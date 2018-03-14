from Bio import Entrez, SeqIO
import time
import primer3
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("output_dir", help="output_directory")
args=parser.parse_args()

with open("temp/list") as f:
    content=f.readlines()
content=[x.strip() for x in content]

for i in range(len(content)):
    content[i]=content[i].split(",")


t7_seq="GCGTAATACGACTCACTATAGGG"

outs=open(args.output_dir.rstrip("/")+"/newprimers.csv", "w")

for gene in content:
    gis=gene[0]
    Entrez.email = 'alon.gelber@childrens.harvard.edu'
  

    request = Entrez.epost("nucleotide",id=gis)
    result = Entrez.read(request)
    webEnv = result["WebEnv"]
    queryKey = result["QueryKey"]
    handle = Entrez.efetch(db="nucleotide",retmode="xml", webenv=webEnv, query_key=queryKey)
    for r in Entrez.parse(handle):
       
        try:
            gi=int([x for x in r['GBSeq_other-seqids'] if "gi" in x][0].split("|")[1])
        except ValueError:
            gi=None


    input_seq = r["GBSeq_sequence"]
    primer = primer3.bindings.designPrimers(
        {

            'SEQUENCE_ID': 'hmhm',
            'SEQUENCE_TEMPLATE': input_seq,
            'SEQUENCE_EXCLUDED_REGION': [0, 0]
        },
        {
            'PRIMER_TASK': 'generic',
            'PRIMER_PICK_LEFT_PRIMER': 1,
            'PRIMER_PICK_INTERNAL_OLIGO': 0,
            'PRIMER_PICK_RIGHT_PRIMER': 1,
            'PRIMER_NUM_RETURN': 5,
            'PRIMER_OPT_SIZE': 20,
            'PRIMER_MIN_SIZE': 18,
            'PRIMER_MAX_SIZE': 25,
            'PRIMER_OPT_TM': 60.0,
            'PRIMER_MIN_TM': 57.0,
            'PRIMER_MAX_TM': 63.0,
            'PRIMER_MIN_GC': 20.0,
            'PRIMER_MAX_GC': 80.0,
            'PRIMER_MAX_POLY_X': 5,
            'PRIMER_SALT_MONOVALENT': 50.0,
            'PRIMER_DNA_CONC': 50.0,
            'PRIMER_MAX_NS_ACCEPTED': 0,
            'PRIMER_MAX_SELF_ANY': 12,
            'PRIMER_MAX_SELF_END': 8,
            'PRIMER_PAIR_MAX_COMPL_ANY': 12,
            'PRIMER_PAIR_MAX_COMPL_END': 8,
            'PRIMER_PRODUCT_SIZE_RANGE': [[200,500]]})
    keyL="PRIMER_LEFT_0_SEQUENCE"
    keyR="PRIMER_RIGHT_0_SEQUENCE"
    outs.write(primer[keyL]+","+gene[1]+"-F"+",Alon,25 nmol\n")
    outs.write(t7_seq+primer[keyR]+","+gene[1]+"-R+T7"+",Alon,25 nmol\n")

outs.close()
