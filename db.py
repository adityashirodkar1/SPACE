from pymongo import MongoClient
connection_string = "mongodb+srv://adishiro:gintoki@cluster0.wlmssnp.mongodb.net/SPACE?retryWrites=true&w=majority"
client = MongoClient(connection_string)
db = client.get_database("SPACE")
users = db.get_collection("users")