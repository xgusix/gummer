import pymongo

aid = '401' # Must be unique
name = "Mongo db connector"
desc = "Connector for the mongo database <db name>."

#Modify with your parameters
HOST = "localhost"
PORT = 27017
DB = "test"
COLLECTION = "test"

def queryDB(query):
    con = pymongo.MongoClient(HOST, 27017)
    db = con[DB]
    cur =  db[COLLECTION].find(query)
    return cur

def launch(query):
    cur = queryDB(query)
    return cur

