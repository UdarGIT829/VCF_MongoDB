import tensorflow as tf

def one_hot_encode_tf(seq:str):
    # Mapping of nucleotides to their encoding, defaulting to 0 for any other character
    mapping = {'A': 1, 'C': 2, 'G': 3, 'T': 4}
    # Convert sequence to numbers, with non-ACGT characters as 0
    seq_num = [mapping.get(nucleotide, 0) for nucleotide in seq]
    # Use one_hot encoding in TensorFlow, adjusting depth to 5 to account for the 'other' category
    one_hot = tf.one_hot(seq_num, depth=5)
    # Remove the first column to ensure non-ACGT characters remain encoded as 0
    one_hot = one_hot[:, 1:]
    return one_hot


