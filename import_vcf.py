import csv

def do1000gpt()-> list:
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

            elif foundHeaders > 0:
                mutation = {    
                    'chr':line[0],
                    'pos':line[1],
                    'ref':line[3],
                    'alt':line[4]
                    }

                if "," in mutation['alt']:
                    mutation['alt'] = mutation['alt'].split(",")
                else:
                    mutation['alt'] = [mutation['alt']]
                for iterSampleTruthIndex in range(len(line[9:])):
                    iterSampleTruth = int(line[9+iterSampleTruthIndex])
                    if iterSampleTruth >= 1:
                        iterSampleName = sampleNames[iterSampleTruthIndex]
                        if samples[iterSampleName].get(mutation['chr']) == None:
                            samples[iterSampleName][mutation['chr']] = {mutation['pos']:f"{mutation['ref']}>{mutation['alt'][iterSampleTruth-1]}"}
                        else:
                            samples[iterSampleName][mutation['chr']][mutation['pos']] = f"{mutation['ref']}>{mutation['alt'][iterSampleTruth-1]}"

    return samples
