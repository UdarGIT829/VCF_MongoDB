import time

def mutate(_ref,_altData):
    seq = ""
    counter = 0
    sorted_mutations = _altData
    for position_checkpoint,mutation_checkpoint in _altData.items():
        position_checkpoint=int(position_checkpoint)   
        print(f"Processing Position {position_checkpoint}",end="\r")     
        seq += _ref[counter:position_checkpoint-1]
        seq += mutation_checkpoint.split(">")[1]
        counter = position_checkpoint-1+len(mutation_checkpoint.split(">")[0])
    return seq


def mutateSamples(samples, _ref):
    output = {}
    times = []  # List to store time taken for each sample

    for sampleID, sampleData in samples.items():
        start_time = time.time()  # Start time for mutation

        # Perform mutation
        output[sampleID] = sampleData
        output[sampleID]['seq'] = mutate(_ref=_ref, _altData=sampleData['MT'])

        end_time = time.time()  # End time for mutation
        times.append(end_time - start_time)  # Calculate and store duration

    # Calculate statistics
    if times:  # Ensure the list is not empty to avoid division by zero
        avg_time_per_sample = sum(times) / len(times)
        max_time_per_sample = max(times)
    else:
        avg_time_per_sample = None
        max_time_per_sample = None

    statistics = {
        "avg_time_per_sample": avg_time_per_sample,
        "max_time_per_sample": max_time_per_sample
    }

    return output, statistics

