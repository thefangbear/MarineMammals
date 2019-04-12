#!/usr/bin/python3
from Bio import SeqIO
from sys import argv
from Bio.Align.Applications import ClustalOmegaCommandline
import re
import csv
# *.py arg1 arg2
if len(argv) != 5:
  print("Usage: " + argv[0] + " <FASTA Input File> <Accession Numbers Txt> <Outgroup accession numbers txt> <FASTA Output File>")
  exit(1)

def get_accessions(name):
  g=None
  with open(name, "r") as fd:
    g = fd.readlines()
    g = list(map(lambda x: x.rstrip(), g))
  return g
  
fasta_in = argv[1]
accession_file = argv[2]
outgroup_file = argv[3]
fasta_out = argv[4]
delimiters = ';', ':', ',', '.', ' ', '(', ')'
regexPattern = '|'.join(map(re.escape, delimiters))
try:
#  with open(accession_file, "r") as fd:
#    _accessions = fd.readlines()
#  with open(outgroup_file, "r") as fd:
#    _outgroup_accessions = fd.readlines()
#  print("read: ", _accessions)
#  for aid in _accessions:
#    accessions.append(aid.rstrip())
#    print("> Added sequence id: ", aid.rstrip())
#  for aid in _outgroup_accessions:
#    outgroup_accessions.append(aid.rstrip())
#    print("* Added outgroup id: ", aid.rstrip())
  accessions = get_accessions(accession_file)
  outgroup_accessions = get_accessions(outgroup_file)
  sequences = list(SeqIO.parse(fasta_in, "fasta"))
  subset_of_sequences = []
  outgroup_keys = []
  for seq in sequences:
    if seq.id.split('.')[0] in accessions:
      print(argv[0] + ': adding ' + seq.id + ' to subset')
      subset_of_sequences.append(seq)
    if seq.id.split(".")[0] in outgroup_accessions:
      outgroup_keys.append("_".join(re.split(regexPattern, seq.description)))
  for seq in subset_of_sequences:
    x = re.split(regexPattern, seq.description)
    seq.id = "_".join(x)
    seq.description = seq.id.split("_")[0]
  print(subset_of_sequences)
  print("Wrote, ", SeqIO.write(subset_of_sequences, fasta_out, "fasta"))
  print("making alignment using clustalo...")
  clustalomega_cline = ClustalOmegaCommandline(infile=fasta_out, outfile=fasta_out, verbose=True, auto=True, force=True)
##  clustalomega_cline.force = True
  print(clustalomega_cline())
  with open("outgroup_keys.txt", "w") as fd:
    fd.writelines(outgroup_keys)
except Error:
  print("An error occured during the process. Please try again.")
  exit(1)

