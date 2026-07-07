from pymongo import MongoClient
connection_string = ""
client = MongoClient(connection_string)
db = client.get_database("SPACE")
users = db.get_collection("users")
