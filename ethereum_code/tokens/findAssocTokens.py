# findAssocTokens.py
# Finds all tokens transacted between the addresses in assocAddresses.csv
# and saves them into assocTokens.csv

import csv
import numpy as np

addresses = []
with open("../../ethereum_data/specialAddresses.csv") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        addresses.append(row[0])
addresses = set(addresses)

tokens = set([])
for i in range(8):
    print("Block number %d" % i)
    with open("../../ethereum_data/token_csvs/token_transfers%d.csv" % i) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            if row[0][0] == 't':
                indicies = {}
                for j in range(len(row)):
                    indicies[row[j]] = j
            else:
                ta = row[indicies["to_address"]]
                fa = row[indicies["from_address"]]
                to = row[indicies["token_address"]]

                if ta in addresses or fa in addresses:
                    tokens.add(to)

tokens = list(tokens)
with open("../../ethereum_data/assocTokens.csv", 'w') as csvfile:
    for token in tokens:
        csvfile.write("%s\n" % token)
