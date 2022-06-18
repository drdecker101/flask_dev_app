import re

def convertOMCtoOFX(cid_input):
    # Convert OMC paths to OFX paths

    path = cid_input.strip() 

    code = "OTE"

    pattern = r"^\d{5,6}\.\w{3,4}\.\w+\.\w+$"

    match = re.match(pattern, path)

    replacer = ["001", "OFX", code, code]

    out = path.split(".")

    new_out = []

    if match :
        for i,j in enumerate(out):

            obj_without_last_two_words = j[:-3]
            new_obj = obj_without_last_two_words + replacer[i]
            new_out.append(new_obj)

        # change FLEX or any other type to OFX
        new_out[1] = replacer[1]

        return ".".join(new_out)

def convertOMCtoGE100L(cid_input, code_input, side_input):
# Convert OMC paths to GE100L paths

    path = cid_input.strip()
    # input_example_2 = "93001.FLEX.MNCHTNEMO60.SVVLTNKAO60"

    # type = input("Enter Site Type (e.g. MCR(M), EDR(E)): ").upper()
    type = code_input.upper()

    site_types = ["MCR", "EDR", "M", "E"]

    site_side = ""

    type = "EDR" if type not in site_types or type is None else type

    pattern = r"^\d{5,6}\.\w{3,4}\.\w+\.\w+$"

    match = re.match(pattern, path)

    site_sides = ["A","Z"]

    if type in ["MCR","M"]:
        # site_side = input("Which side is the MCR site? A side or Z side?: ").upper()
        site_side = side_input.upper()

        site_side = "A" if site_side not in site_sides or site_side is None else site_side

    replacer = ["001", "GE100L", "1CW", "1CW"]

    out = path.split(".")

    new_out = []

    if match :
        for i,j in enumerate(out):

            if i == 1 and len(j) > 3 :
                new_obj = replacer[1]
                new_out.append(new_obj)
            else:
                obj_without_last_two_words = j[:-3]
                new_obj = obj_without_last_two_words + replacer[i]
                new_out.append(new_obj)

        print(site_side)
        if site_side == "A":
            new_out[2] = "MCR01" + new_out[2][:-3]
        elif site_side == "Z":
            new_out[3] = "MCR01" + new_out[3][:-3]   
            new_out[2], new_out[3] = new_out[3], new_out[2]


        print("#"*40)
        print(".".join(new_out))
        print("#"*40)

        return ".".join(new_out)

def replicate(input1, input2, rangeR):
    
    store = []
    for n in range(rangeR+1):
        if input1 == "BE" and n < 10:
            out = f"{input1}20{n}/{input2}20{n} 100G"
        elif input1 == "BE":
            out = f"{input1}2{n}/{input2}2{n} 100G"
        elif n < 10:
            out = f"{input1}10{n}/{input2}10{n} 100G"
        else:
            out = f"{input1}1{n}/{input2}1{n} 100G"
        store.append(out)

    return store

def convertLAGtoTSV(path, ces):

    store = []
    
    pattern = r"^\d{5,6}\.\w{4,6}\.\w+\.\w+$"

    match = re.match(pattern, path)

    if match:

        out = path.split(".")

        tid = out[2]
        np = out[0]

        edr_tsv_1 = f"{np}.ME100.{tid}.{tid[:-3]}D0T"
        edr_tsv_2 = f"{int(np)+ 1}.ME100.{tid}.{tid[:-3]}D0T"
        

        ons_tsv = f"{np}.ME100.{tid[:-3]}OTE.{tid[:-3]}D0T"
        tsv_cbo = f"{np}.GE1.{tid[:-3]}01Y.{tid[:-3]}D0T"
        tsv_tsv = f"{np}.ME100.{tid[:-3]}01X.{tid[:-3]}D0T"

        store.append(f"EDR <> TSV path 1: {edr_tsv_1}\n")
        store.append(f"EDR <> TSV path 2: {edr_tsv_2}\n")
        store.append(f"ONS <> TSV path : {ons_tsv}\n")
        store.append(f"TSV <> CBO path : {tsv_cbo}\n")
        store.append(f"TSV <> TSV path : {tsv_tsv}\n")
        
    if ces == "Yes":
        edr_ces = f"{np}.GE100L.{tid}.{tid[:-3]}2QW"
        ces_tsv =f"{np}.ME100.{tid[:-3]}2QW.{tid[:-3]}D0T"

        store.append(f"TSV <> CBO path : {edr_ces}\n")
        store.append(f"TSV <> CBO path : {ces_tsv}\n")
        


    return store
