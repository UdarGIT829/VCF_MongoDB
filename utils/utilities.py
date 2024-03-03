from Bio import Entrez, SeqIO
import requests
import json
import os

url = "http://127.0.0.1:5000"


def get_refSEQ(accession:str) -> str:
    """ Check if the reference genome is in the database by name.
            Y-> Return the str of the reference genome
            N-> Retrieve the file from NCBI, them import it into the database 
    
    """
    response = requests.get(f"{url}/references")

    if response.status_code == 200:
        print("Reference list get success:")
        print(response.json())
    else:
        print(f"Reference list get fail with status code {response.status_code}")
    _ref_list = response.json()

    print(_ref_list)
    print(accession)
    if any(accession == iterRefData.get('_id') for iterRefData in _ref_list):
        params = {"query":{"_id":accession}}
        response = requests.get(url=f"{url}/query_ref", json=params)
    else:
        print(f"Accession {accession} not in db, querying NCBI...")
        retrieve_ref_file(accession=accession)
        params = {"query":{"_id":accession}}
        response = requests.get(url=f"{url}/query_ref", json=params)

    if response.status_code == 200:
        print("Reference get success:")
        print(str(response.json())[0:100]+"...")
    else:
        print(f"Reference get fail with status code {response.status_code}")


    result = response.json()["seq"]

    return result

# Set your email here
Entrez.email = "example@example.com"

def retrieve_ref_file(accession = "NC_012920.1"):
    # Define the accession number for the Homo sapiens mitochondrion, complete genome
    # accession = "NC_012920.1"
    ref_path = f"./ref/{accession}.txt"

    # Use Entrez.efetch to download the sequence data from NCBI
    with Entrez.efetch(db="nucleotide", rettype="fasta", retmode="text", id=accession) as handle:
        # Read the sequence record
        seq_record = SeqIO.read(handle, "fasta")


    params = {
                "collection":"ref_store",
                "data":{
                    "_id":accession,
                    "seq":str(seq_record.seq)
                }
              }
    response = requests.post(url=f"{url}/insert_one", json=params)

    if response.status_code == 200:
        print("Insertion call success:")
        print(response.json())
    else:
        print(f"Insertion failed with status code {response.status_code}")

    return response.status_code