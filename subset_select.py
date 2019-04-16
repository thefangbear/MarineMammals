#!/usr/bin/python3
from Bio import SeqIO
from sys import argv
from Bio.Align.Applications import ClustalOmegaCommandline
import re
import csv
# *.py arg1 arg2
if len(argv) != 5:
  print("Usage: " + argv[0] + " <FASTA Input File> <Accession Numbers Txt> <User-friendly names txt> <FASTA Output File>")
  exit(1)

accession_description = {}

def get_accessions(name):
  g=None
  with open(name, "r") as fd:
    g = fd.readlines()
    g = list(map(lambda x: x.rstrip(), g))
  return g
  
fasta_in = argv[1]
accession_file = argv[2]
userfriendly_file = argv[3]
fasta_out = argv[4]
delimiters = ';', ':', ',', '.', ' ', '(', ')'
regexPattern = '|'.join(map(re.escape, delimiters))
try:
  accessions = get_accessions(accession_file)
  userfriendly = get_accessions(userfriendly_file)
  sequences = list(SeqIO.parse(fasta_in, "fasta"))
  subset_of_sequences = []
  outgroup_keys = []

  for us in userfriendly:
    aus = us.split(':')  
    if (len(aus) < 3): 
      break
    accession_description[aus[0].rstrip()] = aus[1] + "__" + "_".join(aus[2].split(" "))

  for seq in sequences:
    if seq.id.split('.')[0] in accessions:
      print(argv[0] + ': adding ' + seq.id + ' to subset')
      subset_of_sequences.append(seq)

  for seq in subset_of_sequences:
    x = re.split(regexPattern, seq.description)
    seq.id = accession_description[seq.id.split('.')[0]] + "_"
    print(seq.id)
    seq.id += "_".join(x[:4]) 
    seq.description = ""
    #seq.description = seq.id.split("_")[0]

  print(subset_of_sequences)
  print("Wrote, ", SeqIO.write(subset_of_sequences, fasta_out, "fasta"))
  print("making alignment using clustalo...")
  clustalomega_cline = ClustalOmegaCommandline(infile=fasta_out, outfile=fasta_out, verbose=True, auto=True, force=True)
  print(clustalomega_cline())
  with open("outgroup_keys.txt", "w") as fd:
    fd.writelines(outgroup_keys)
except Error:
  print("An error occured during the process. Please try again.")
  exit(1)

