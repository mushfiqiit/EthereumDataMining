import networkx as nx
import pandas as pd
import numpy as np
import csv

inputFile = "tokenGraph/corrEdgesPrice.csv"
outputFile = "tokenGraph/corrEdgesTree.csv"

G = nx.Graph()

names = set()
edges = []
with open(inputFile) as infile:
    reader = csv.reader(infile)
    for row in reader:
        if len(row) == 0:
            continue
        #if row[0][0] == '0':
        if row[0] != "Source":
            fa = row[0]
            ta = row[1]
            va = float(row[2])
            names.add(fa)
            names.add(ta)
            edges.append((fa,ta,va))

G.add_nodes_from(list(names))
G.add_weighted_edges_from(edges)

MG = nx.maximum_spanning_tree(G)

with open(outputFile, 'w') as outfile:
    outfile.write("Source,Target\n")
    for (s,t) in MG.edges():
        outfile.write("%s,%s\n" % (s,t))
