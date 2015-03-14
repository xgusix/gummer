import sqlite3

aid = '201' # Must be unique
name = "Sqlite db connector"
desc = "Connector for the sqlite database test.db.\n Returs a the cursor."

#Modify with your parameters
DB = '/home/xgusix/Projects/gummer/test.db'

def queryDB(query):
	rows = None
	con = sqlite3.connect(DB)

	with con:
		cur = con.cursor()   
		cur.execute(query)

	return cur

def launch(query):
	cur = queryDB(query)
	return cur