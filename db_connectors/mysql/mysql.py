import MySQLdb

aid = '101' # Must be unique
name = "Mysql db connector"
desc = "Connector fpr the mysql database <db name>."

#Modify with your parameters
HOST = "localhost"
USER = "root"
PASSWD = "root"
DB = "trader"

def queryDB(query):
	rows = None
	con = MySQLdb.connect(host = HOST,
						user = USER,
						passwd = PASSWD,
						db = DB)
	with con:
		cur = con.cursor() 
		cur.execute(query)

	return cur

def launch(query):
	cur = queryDB(query)
	return cur