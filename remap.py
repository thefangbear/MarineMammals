#!/usr/bin/python3
# remap.py - remap nodes with accession IDs in a newick tree to human-readable format
from Bio import Phylo
from Bio import SeqIO

if len(argv) != 3: 
  print("Usage: ", argv[0], " <fasta file> <newick file> <new tree file>")
  exit(1)

sequences = list(SeqIO.read(argv[1], "fasta"))
tree = Phylo.read(argv[2], "newick")

# remap node names


# output tree

