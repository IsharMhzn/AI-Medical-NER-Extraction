from pymongo import MongoClient
import json

client = MongoClient('localhost', 27017)

db = client["medical_ai"]
mycol = db["medical_records"]

with open("medical-cases-data.json") as f:
    data = json.load(f)


medical_records = [v for v in data.values()]
mycol.insert_many(medical_records)