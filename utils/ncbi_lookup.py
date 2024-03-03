import re
from Bio import Entrez

def fetch_mitochondrial_gene_info(position, accession="NC_012920", email="example@example.com"):
    """
    Fetch gene information at a specified position from the mitochondrial genome.
    
    Parameters:
    - position (str): The nucleotide position in the mitochondrial genome.
    - accession (str): The accession number for the mitochondrial genome. Default is NC_012920.
    - email (str): The email to use for Entrez.
    
    Returns:
    - A dictionary containing structured gene information.
    """
    # Set your NCBI E-utilities email
    Entrez.email = email

    try:
        record = None
        data = {}
        heading = None
        with Entrez.efetch(db="nucleotide", id=accession, rettype="gb", retmode="text", seq_start=position, seq_stop=position) as handle:
            record = str(handle.read())
        record_lines = record.splitlines()
        
        for line in record_lines:
            # Split the line on any combination of two or more spaces
            split_line = re.split(r'\s{2,}', line)
            if len(split_line) > 1:
                if split_line[0] == '':
                    if split_line[1].isupper() and " " not in split_line[1]:
                        if len(split_line) > 2:
                            subheadingTitle = split_line[1]
                            data[heading][subheadingTitle] = {"text": split_line[2]}
                            continue

                    if data[heading].get("text") != None:
                        data[heading]["text"] += " " + split_line[1]
                    else:
                        data[heading]["text"] = split_line[1]
                else:
                    if split_line[0].isupper():
                        heading = split_line[0]
                        data[heading] = {}
                    data[heading]["text"] = split_line[1]
        return data
    except Exception as e:
        print(f"An error occurred: {e}")
        return {}

