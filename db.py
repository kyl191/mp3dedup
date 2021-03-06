import sqlite3

def createDB(dbPath):
	conn = sqlite3.connect(dbPath)
	conn.text_factory = unicode
	c = conn.cursor()
	c.execute("""CREATE TABLE mp3dedup (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "id3_title" TEXT,
    "id3_artist" TEXT,
    "id3_album" TEXT,
    "strippedhash" TEXT,
    "originalhash" TEXT,
    "filepath" TEXT,
    "mtime" INTEGER)""")

def startDB(dbPath):
	try:
		conn = sqlite3.connect(dbPath)
		conn.text_factory = unicode
		c = conn.cursor()
		c.execute("SELECT * from mp3dedup")
	except sqlite3.OperationalError as e:
		print("SQLite3 Error : Operational Error", e.args[0])
	except sqlite3.DatabaseError as e:
		print("SQLite3 Error : Database Error", e.args[0])
	except sqlite3.Error as e:
		print("SQLite 3: Unknown Error", e.args[0])
	except:
		print("Unknown Error")
	return conn

def insertIntoDB(db, info):
	# info = title, artist, album, strippedhash, originalhash, filepath, mtime
	try:
		db.execute(u"INSERT into mp3dedup VALUES (Null, ?, ?, ?, ?, ?, ?, ?)",info)
	except sqlite3.Error as e:
		print("SQLite 3: Unknown Error", e.args[0])
	return info

def checkIfExists(db,filepath):
	try:
		(results,) = db.execute(u"SELECT COUNT(*) from mp3dedup WHERE filepath = ?",[filepath])
	except sqlite3.Error as e:
		print("SQLite 3: Unknown Error", e.args[0])
	else:
		if results[0] > 0:
			(mtime,) = db.execute(u"SELECT mtime from mp3dedup WHERE filepath = ?",[filepath])
			return (results[0],mtime[0])
		else:
			return (0, -1)
def updateDB(db, info):
	# info = title, artist, album, hash, filepath, mtime
	try:
		db.execute(u"UPDATE mp3dedup set id3_title = :title, id3_artist = :artist, id3_album = :album, hash = :hash, mtime = :mtime where filepath = :path",
			{"title":info.title, "artist":info.artist, "album":info.album, "hash":info.hash, "mtime":info.mtime, "path":info.filepath})
	except sqlite3.Error as e:
		print("SQLite 3: Unknown Error", e.args[0])
	return info
