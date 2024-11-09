import csv
from pymongo import MongoClient

def generate_hsd_file(sample_id, output_file='output.hsd'):
    """
    Generates an HSD file for a selected sample from MongoDB.

    Args:
        sample_id (str): The unique identifier of the sample.
        output_file (str): The name of the output HSD file.

    Returns:
        bool: True if file generation was successful, False otherwise.
    """
    # Connect to MongoDB (update connection string as needed)
    client = MongoClient('mongodb://localhost:27017/')
    db = client['vcfs']  # replace with your MongoDB database name
    collection = db['vcf_refLinked']  # replace with your MongoDB collection name

    # Retrieve sample data
    sample_data = collection.find_one({"_id": sample_id})
    print(sample_data)
    
    # Check if sample exists and contains MT chromosome data
    if not sample_data or 'chromosomes' not in sample_data or 'MT' not in sample_data['chromosomes']:
        print(f"Sample with ID {sample_id} not found or does not contain MT chromosome data.")
        return False
    
    # Extract HSD data for mitochondrial chromosome
    mt_data = sample_data['chromosomes']['MT']
    ref_id = mt_data.get("refID", "NC_012920.1")  # Default reference ID if not present
    
    # Prepare polymorphisms in HSD format
    polymorphisms = []
    for position, mutation in mt_data.items():
        if position != "refID":
            # Format mutation as "<position><alt_base>"
            position_only, mutation_code = mutation.split("->")
            polymorphisms.append(f"{position}{mutation_code[-1]}")
    
    # Generate HSD file format
    hsd_content = {
        "ID": sample_id,
        "Range": "1-16569",  # Assuming full mitochondrial range
        "Haplogroup": "?",   # Placeholder, as it’s not specified in the sample data
        "Polymorphisms": "\t".join(polymorphisms)
    }
    
    # Write to HSD file
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter='\t')
        writer.writerow(hsd_content.keys())  # Write header
        writer.writerow(hsd_content.values())  # Write data

    print(f"HSD file generated: {output_file}")
    return True

if __name__ == "__main__":
    generate_hsd_file("HG00096", "sample_HG00096.hsd")
