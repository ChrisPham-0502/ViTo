from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
VitoDB = client["VitoDB"]
usersDB = VitoDB["usersDB"]
