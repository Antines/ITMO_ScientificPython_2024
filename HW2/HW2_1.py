import requests
import json
import re

########################################################################################################################
#                                                        I
########################################################################################################################

def get_ensembl(ids):
    server = "https://rest.ensembl.org"
    ext = "/lookup/id"
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    data = json.dumps({ "ids" : ids })

    print("API Request:")
    print("URL:", server + ext)
    print("Headers:", headers)
    print("Data:", data)
    print()

    return requests.post(server + ext, headers=headers, data=data).json()

def parse_response_ensembl(response):
    for gene_id, info in response.items():
        print(f"Gene ID: {gene_id}")
        print("Gene Info")
        for key, value in info.items():
            print(f"    {key}: {value}")
        print()

#ids = ["ENSG00000157764", "ENSG00000248378"] #list(map(str, input().split(",")))
#response = get_ensembl(ids)
#print(parse_response_ensembl(response))


def get_uniprot(ids):
    accessions = ids
    endpoint = "https://rest.uniprot.org/uniprotkb/accessions"
    params = {'accessions': accessions}

    print("API Request:")
    print("URL:", endpoint)
    print("Parameters:", params)
    print()

    return requests.get(endpoint, params=params).json()

def parse_response_uniprot(response):
    output = ""
    for val in response ["results"]:
        acc = val.get('primaryAccession', '')
        species = val.get('organism', {}).get('scientificName', '')
        gene = val.get('genes', [])
        seq = val.get('sequence', '')
        output += f"Accession: {acc}\n"
        output += f"Organism: {species}\n"
        output += f"Gene Info: {gene}\n"
        output += f"Sequence Info: {seq}\n"
        output += "Type: Protein\n\n"

    return output

#ids = ['P11473', 'P13053'] #list(map(str, input().split(",")))
#response = get_uniprot(ids)
#print(parse_response_uniprot(response))

########################################################################################################################
#                                                        II
########################################################################################################################

def process_ids(ids):
    uni = r'^[OPQ][0-9][A-Z0-9]{3}[0-9]|[A-NR-Z][0-9]([A-Z][A-Z0-9]{2}[0-9]){1,2}$'
    ens = r'^ENS[A-Z]+[0-9]{11}$'

    uniprot_ids = []
    ensembl_ids = []

    for id in ids:
        if re.match(uni, id):
            uniprot_ids.append(id)
        elif re.match(ens, id):
            ensembl_ids.append(id)

    parsed = {}

    if uniprot_ids:
        uniprot_response = get_uniprot(uniprot_ids)
        uniprot_parsed = parse_response_uniprot(uniprot_response)
        parsed['Uniprot'] = uniprot_parsed

    if ensembl_ids:
        ensembl_response = get_ensembl(ensembl_ids)
        ensembl_parsed = parse_response_ensembl(ensembl_response)
        parsed['Ensembl'] = ensembl_parsed

    return parsed

ids = ["ENSG00000157764", "ENSG00000248378"] #list(map(str, input().split(",")))
for db, data in process_ids(ids).items():
    print(f"Database: {db}")
    print(data)
    print()