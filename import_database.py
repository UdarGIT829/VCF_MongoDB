from pymongo import errors
import csv # for parsing the vcf
import sys # for memory size statistics
import import_vcf

from utilities import *

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


