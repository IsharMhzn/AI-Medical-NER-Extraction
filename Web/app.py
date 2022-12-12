from flask import Flask, request, render_template, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps

import json

app = Flask(__name__)
client = MongoClient('localhost', 27017)

db = client["medical_ai"]
mycol = db["medical_records"]

@app.route("/")
def get_medical_records():
    age = request.args.get("age")
    disease = request.args.get("disease")
    gender = request.args.get("gender")
    meds = request.args.get("medicine")

    query = {}
    if age or disease or gender or meds:
        query["$and"] = []
    if age:
        query["$and"].append({"AGE": {"$regex": age}})
    if disease:
        query["$and"].append({"DIAGNOSIS": {"$regex": disease}})
    if gender:
        query["$and"].append({"GENDER": {"$regex": gender}})
    if meds:
        query["$and"].append({"MEDICATION": {"$regex": meds}})

    docs = mycol.find(query)
    data = {}
    for i, doc in enumerate(docs):
        data[i] = doc
        data[i]["_id"] = str(data[i]["_id"])       
    return render_template("index.html", patients=data)

@app.route("/<patient_id>")
def get_patient_detail(patient_id):
    patient = mycol.find_one({"_id": ObjectId(f'{patient_id}')})
    patient = json.loads(dumps(patient))
    patient["_id"] = patient["_id"]["$oid"]
    return render_template("patienthistory.html", patient=patient)

if __name__ == "__main__":
    app.run(debug=True)