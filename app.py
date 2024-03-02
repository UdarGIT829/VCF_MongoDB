from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
import json

import mutator
from utilities import *

app = Flask(__name__)

# MongoDB configuration
app.config["MONGO_URI"] = "mongodb://localhost:27017/vcfs"
mongo = PyMongo(app)

# Feature: Get all sample names
@app.route('/getAllSampleNames', methods=['GET'])
def get_all_sample_names():
    # Query the database for ids
    results = mongo.db["vcf_refLinked"].find({}, {'_id': 1})
    # Convert results to a list of dicts
    results_list = list(results)
    
    # Return the results as JSON
    return jsonify(results_list)

# Feature: Import VCF to DB
@app.route('/importVCF', methods=['POST'])
def import_vcf_to_db():
    data = request.json.get("data")

    selectedCollection = request.json.get("collection")

    if selectedCollection == None:
        selectedCollection = "vcf_refLinked"

    result = mongo.db[selectedCollection].insert_one(data)
    return jsonify({"result": "success", "document_id": str(result.inserted_id)})

# Feature: Export DB to VCF
@app.route('/exportDBtoVCF', methods=['GET'])
def export_db_to_vcf():
    # Implement the logic to export data from DB to a VCF file
    # Return the VCF file and a response code
    pass

# Feature: Get Sample JSON
@app.route('/getSampleJSON', methods=['GET'])
def get_sample_json():
    # Implement the logic to retrieve a sample's JSON representation
    # Return the JSON and a response code
    pass

# Feature: Export JSON
@app.route('/exportJSON', methods=['GET'])
def export_json():
    # Implement the logic to export data as JSON file
    # Return the JSON file and a response code
    pass

# Feature: Get References
@app.route('/getReferences', methods=['GET'])
def get_references():
    # Implement the logic to get all references
    # Return a list of references and a response code
    pass

# Feature: Get Reference Sequence
@app.route('/getRef', methods=['GET'])
def get_ref():
    # Implement the logic to get a specific reference sequence
    # Return the reference sequence and a response code
    pass

# Feature: Set Value
@app.route('/setValue', methods=['POST'])
def set_value():
    # Implement the logic to set a specific value in a sample
    # Return a response code indicating success or failure
    pass

# Feature: Mutate Sample
@app.route('/mutateSample', methods=['POST'])
def mutate_sample():
    # Implement the logic to mutate a sample
    # Return the mutated sample sequence and a response code
    pass

if __name__ == '__main__':
    app.run(debug=True)
