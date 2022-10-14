from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/project1_fastapi')
mdb = client.project1_fastapi