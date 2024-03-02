import csv
import glob

# For carriage return in printing
# import sys

def do1000gpt()-> dict:
    sampleNames = list()
    headers = list()

    samples = dict()

    vcf_files_path = 'vcf/*.vcf'
    vcf_files = glob.glob(vcf_files_path)

    for vcf_file in vcf_files:
        print(f'Opening file: {vcf_file}')
        with open(vcf_file, 'r') as fi:
            print(f'Processing file: {vcf_file}')
            reader = csv.reader(fi, delimiter="\t")
            _refID = "PLACEHOLDER REFID"
            foundHeaders = False
            lineIndex = 0
            for line in reader:
                print(f'Processing line: {lineIndex+1}', end="\r")
                # sys.stdout.flush()
                # print(f"Line: {line}")
                lineIndex += 1

                if "#CHROM" in line[0]:
                    foundHeaders = True
                    headers = line[0:8]
                    sampleNames = line[9:]
                    for iterSample in sampleNames:
                        samples[iterSample] = {
                            '_id': iterSample,
                            'data_src': '1000gpt',
                            'tags': '',
                            'chromosomes': dict()
                        }
                elif not foundHeaders:
                    if "#reference" in line[0]:
                        ref_info = line[0].replace("##reference=", "").split("|")
                        for iterItemIndex in range(len(ref_info)):
                            iterItem = ref_info[iterItemIndex]
                            if "ref" == iterItem:
                                _refID = ref_info[iterItemIndex + 1]
                                break

                elif foundHeaders:
                    process_mutation(line, sampleNames, samples, _refID)
                    pass

    print()
    return samples

def process_mutation(line, sampleNames, samples, _refID):
    mutation = {
        'chr': line[0],
        'pos': line[1],
        'ref': line[3],
        'alt': line[4]
    }

    if "," in mutation['alt']:
        mutation['alt'] = mutation['alt'].split(",")
    else:
        mutation['alt'] = [mutation['alt']]
    for iterSampleTruthIndex in range(len(line[9:])):
        
        iterSampleTruth = line[9+iterSampleTruthIndex]
        iterSampleName = sampleNames[iterSampleTruthIndex]
        _iterValue = None

        if "|" in iterSampleTruth:
            if "1" in iterSampleTruth:
                _iterValue = iterSampleTruth
            else:
                continue
        else:
            iterSampleTruth = int(iterSampleTruth)
            if iterSampleTruth >= 1:
                _iterValue = f"{mutation['ref']}->{mutation['alt'][iterSampleTruth-1]}"

        if _iterValue != None:
            iterSampleName = sampleNames[iterSampleTruthIndex]
            if not samples[iterSampleName]['chromosomes'].get(mutation['chr']):
                samples[iterSampleName]['chromosomes'][mutation['chr']] = {mutation['pos']: _iterValue}
            else:
                samples[iterSampleName]['chromosomes'][mutation['chr']][mutation['pos']] = _iterValue

            if not samples[iterSampleName]['chromosomes'][mutation['chr']].get(_refID):
                samples[iterSampleName]['chromosomes'][mutation['chr']]['refID'] = _refID

    return samples
