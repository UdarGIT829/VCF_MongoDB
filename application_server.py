from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
import json

import mutator
from utilities import *

app = Flask(__name__)

# MongoDB configuration
app.config["MONGO_URI"] = "mongodb://localhost:27017/vcfs"
mongo = PyMongo(app)

# Route to query the database
@app.route('/query', methods=['GET'])
def query_db():
    # Extract query parameters
    params = request.args.to_dict()
    query_params = json.loads(request.args.get('query'))

    # Query the database
    results = mongo.db["vcf_refLinked"].find(query_params)
    # Convert results to a list of dicts
    results_list = list(results)
    if params.get("do mutation") != None:
        _ref = get_refSEQ(r"ref\GRCh38.txt")
        for iterResult in results_list:
            iterResult["seq"] = mutator.mutate(_ref=_ref, _altData=iterResult['MT'])
    # Return the results as JSON
    return jsonify(results_list)

# Route to insert a single document into the database
@app.route('/insert_one', methods=['POST'])
def insert_one():
    data = request.json
    result = mongo.db["vcf_refLinked"].insert_one(data)
    return jsonify({"result": "success", "document_id": str(result.inserted_id)})

# Route to insert many documents into the database
@app.route('/insert_many', methods=['POST'])
def insert_many():
    data = request.json  # Expect a list of documents
    if not isinstance(data, list):
        return jsonify({"error": "Expected a list of documents"}), 400
    result = mongo.db["vcf_refLinked"].insert_many(data)
    return jsonify({"result": "success", "document_ids": [str(id) for id in result.inserted_ids]})

if __name__ == '__main__':
    app.run(debug=True)