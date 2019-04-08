#!/usr/bin/python3

# turn fasta file to nexus file
from Bio import SeqIO
from sys import argv
from Bio.Alphabet import IUPAC

if len(argv) != 3:
  print("usage: ", argv[0], " <fasta file> <nexus file>")
  exit(1)

SeqIO.convert(argv[1], "fasta", argv[2], "nexus", alphabet=IUPAC.unambiguous_dna)
