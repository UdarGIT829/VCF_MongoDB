def get_refSEQ(filename:str):
    result = []
    with open(filename,"r") as fi:
        result = fi.readlines()
    _ref = ""
    for line in result:
        if ">" in line:
            continue
        _ref += line.rstrip()
    return _ref
