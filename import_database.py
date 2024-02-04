from pymongo import MongoClient, errors
import csv # for parsing the vcf
import sys # for memory size statistics

from utilities import *


_ref = get_refSEQ(r"ref\GRCh38.txt")


def getFromRef(requestedPosition:int):
    """
    Will get the requested basepair, later can define which ref to pull from

    For now return "_"
    """
    return "_"

def import_1000gpt():
    sampleNames = list()
    headers = list()

    batch_data = list()
    data = dict()

    _chrms = [""]
    with open(r"vcf\ALL.chrMT.phase3_callmom-v0_4.20130502.genotypes.vcf", "r") as fi:
        reader = list(csv.reader(fi, delimiter="\t"))
        samples = dict()
        foundHeaders = 0
        for lineIndex in range(len(reader)):
            line = reader[lineIndex]
            if "#CHROM" in line[0]:
                foundHeaders = lineIndex
                headers = line[0:8]
                sampleNames = line[9:]
                for iterSample in sampleNames:
                    samples[iterSample] = {
                        '_id': iterSample,
                        'data_src': '1000gpt',
                        'refID': 'GRCh38',
                        'tags':'',
                    }
                # print(sampleNames[0])
            elif foundHeaders > 0:
                mutation = {    
                    'chr':line[0],
                    'pos':line[1],
                    'ref':line[3],
                    'alt':line[4]
                    }
                # print()
                # print(mutation)
                # print()
                # print(_ref[int( mutation['pos'])-1 ])
                # time.sleep(1.0)
                # print(line[0:8])
                if "," in mutation['alt']:
                    mutation['alt'] = mutation['alt'].split(",")
                else:
                    mutation['alt'] = [mutation['alt']]
                for iterSampleTruthIndex in range(len(line[9:])):
                    iterSampleTruth = int(line[9+iterSampleTruthIndex])
                    if iterSampleTruth >= 1:
                        iterSampleName = sampleNames[iterSampleTruthIndex]
                        # print(mutation['alt'])
                        if samples[iterSampleName].get(mutation['chr']) == None:
                            samples[iterSampleName][mutation['chr']] = {mutation['pos']:f"{mutation['ref']}>{mutation['alt'][iterSampleTruth-1]}"}
                        else:
                            samples[iterSampleName][mutation['chr']][mutation['pos']] = f"{mutation['ref']}>{mutation['alt'][iterSampleTruth-1]}"

    return samples

def insertSamplesToCollection(collection, samples):
    # Insert the document
    try:
        insert_result = collection.insert_many(samples.values(), ordered=False)
        # Process insert_result as needed
    except errors.BulkWriteError as bwe:
        # Here you can parse bwe.details to understand what went wrong
        # For example, extract information about duplicate documents
        error_details = bwe.details.get('writeErrors', [])
        print(f"{bwe.details.get('nInserted', [])} Documents inserted")

        for error in error_details:
            # Process each error (this is where you can log or take action on errors)
            # Example: error['errmsg'] contains the error message
            if error['code'] == 11000:
                # print(f"Duplicate ID not inserted: {error['keyValue']['_id']}")
                pass
            else:
                print(error)
                exit()
        # If you need to notify the user or log the overall error quietly, do it here
    except Exception as e:
        # Handle other exceptions, e.g., network issues, authentication errors, etc.
        pass


imported_samples = import_1000gpt()

# Step 1: Connect to the MongoDB - adjust the IP and port as necessary
client = MongoClient('localhost', 27017)

# Step 2: Create or switch to your database
db = client['vcfs']

# Step 3a: Create or switch to your collection
collection = db['vcf_refLinked']

insertSamplesToCollection(collection=collection, samples=imported_samples)

