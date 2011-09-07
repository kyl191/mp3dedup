import db, os, sys, re
from os.path import join, getsize
# Initial setup of DB & search path
dbPath = os.path.abspath("mp3dedup.db")
if not os.path.isfile(dbPath):
	db.createDB(dbPath)
dbconn = db.startDB(dbPath)
dbcursor = dbconn.cursor()
# End initial setup

size = 0
results = dbcursor.execute("""SELECT filepath, COUNT(hash) FROM mp3dedup GROUP BY hash HAVING ( COUNT(hash) > 1 )""")
for result in results:
	dupSize = os.path.getsize(result[0])
	dupCount = result[1]-1
	dupSpace = dupSize * dupCount
	# print result[0],dupSpace
	size = size + dupSpace
print "Total space used by dups: ", size, size/1024,"KB ", (size/1024)/1024, "MB", ((size/1024)/1024)/1024, "GB"
