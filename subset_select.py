#!/usr/bin/python3
from Bio import SeqIO
from sys import argv
from Bio.Align.Applications import ClustalOmegaCommandline
# *.py arg1 arg2
if len(argv) != 4:
  print("Usage: " + argv[0] + " <FASTA Input File> <Accession Numbers Txt> <FASTA Output File>")
  exit(1)

fasta_in = argv[1]
accession_file = argv[2]
fasta_out = argv[3]
_accessions = []
accessions = []
try:
  with open(accession_file, "r") as fd:
    _accessions = fd.readlines()
#  print("read: ", _accessions)
  for aid in _accessions:
    accessions.append(aid.rstrip())
    print("> Added sequence id: ", aid.rstrip())
  sequences = list(SeqIO.parse(fasta_in, "fasta"))
  subset_of_sequences = []
  for seq in sequences:
    if seq.id.split('.')[0] in accessions:
      print(argv[0] + ': adding ' + seq.id + ' to subset')
      subset_of_sequences.append(seq)
  print("Wrote, ", SeqIO.write(subset_of_sequences, fasta_out, "fasta"))
  print("making alignment using clustalo...")
  clustalomega_cline = ClustalOmegaCommandline(infile=fasta_out, outfile=fasta_out, verbose=True, auto=True)
  print(clustalomega_cline)
except Error:
  print("An error occured during the process. Please try again.")
  exit(1)

