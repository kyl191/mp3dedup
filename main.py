import db, hash, mp3, os, sys, re
from os.path import join
from collections import namedtuple
mp3info = namedtuple('mp3info', "title artist album strippedhash originalhash filepath mtime")

def hashAndAdd(file):
	# Check if it's a valid MP3 file first by trying to get the ID3 info
	try:
		title, artist, album = mp3.getid3(file)
	except Exception as e:
		# So far the only exception is an invalid ID3 header found, so not much to grab
		print(e)
		return
	mtime = os.path.getmtime(file)
	(exists,dbmtime) = db.checkIfExists(dbcursor, unicode(str(os.path.abspath(file)).decode('utf-8')))
	update = False
	# Gets back a tuple with (count of rows, mtime)
	# Check if the file has already been hashed
	if exists > 0:
		# If the file hasn't been modified since it was checked, don't bother hashing it
		if dbmtime >= mtime:
			return
		else:
			# Need to come up with an update statement...
			print("Updating", file)
			update = True
	
	tempfile = mp3.stripid3(file)
	strippedhash = hash.sha512file(tempfile[1])
	os.close(tempfile[0])
	os.remove(tempfile[1])
	originalhash = hash.sha512file(file)
	info = mp3info(title, artist, album, unicode(strippedhash), unicode(originalhash), unicode(str(os.path.abspath(file)).decode('utf-8')), mtime)
	if not update:
		print(info,"Ins")
		db.insertIntoDB(dbcursor, info)
	else:
		#print(info,"upd")
		db.updateDB(dbcursor, info)
	dbconn.commit()

# Initial setup of DB
# We keep the connection & cursor seperate so we can do commits when we want
dbPath = os.path.abspath("mp3dedup.db")
if not os.path.isfile(dbPath):
	db.createDB(dbPath)
dbconn = db.startDB(dbPath)
dbcursor = dbconn.cursor()
# End initial setup

# Walk the directory structure looking for MP3 files
for root, subfolders, files in os.walk(sys.argv[1]):
	# Mention what path we're working in.
	print("Working in", os.path.abspath(root))
	# Since root contains the working folder, and we'll move onto subfolders later, 
	# We only care about the filename
	for filename in files:
		# So, for each file, check if it has an MP3 extension
		if re.search(".mp3",filename,re.IGNORECASE):
			# If is does, hash & add it to the db
			hashAndAdd(os.path.abspath(join(root,filename)))
			#print "found MP3 file: ", os.path.abspath(join(root,filename))

# Close the cursor & commit the DB one last time just for good measure
dbcursor.close()
dbconn.commit()
