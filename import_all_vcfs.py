from utils import import_database
from utils import import_vcf
from pymongo import MongoClient


imported_samples = import_vcf.do1000gpt()

# Step 1: Connect to the MongoDB - adjust the IP and port as necessary
client = MongoClient('localhost', 27017)

# Step 2: Create or switch to your database
db = client['vcfs']

# Step 3a: Create or switch to your collection
collection = db['vcf_refLinked']

# print(imported_samples)

import_database.insertSamplesToCollection(collection=collection, samples=imported_samples)