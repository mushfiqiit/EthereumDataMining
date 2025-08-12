# findUserAddresses.py
# Finds a unique set of all token names

import numpy as np
import sys
import csv

csv.field_size_limit(sys.maxsize)

tokens = set([])
indices = {}

for i in range(8):
    print(i)
    with open("../../ethereum_data/token_csvs/token_transfers%d.csv" % i) as csvfile: 
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0][0] == 't':
                for i in range(len(row)):
                    indices[row[i]] = i
            else:
                ta = row[indices["to_address"]]
                fa = row[indices["from_address"]]
                tokens.add(ta)
                tokens.add(fa)

with open("../../ethereum_data/userAddresses.csv", "w") as csvfile:
    for token in tokens:
        csvfile.write("%s\n" % token)
