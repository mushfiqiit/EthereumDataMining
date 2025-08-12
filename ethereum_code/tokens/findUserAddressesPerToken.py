# findUserAddresses.py
# Finds a unique set of all token names

import numpy as np
import sys
import csv

csv.field_size_limit(sys.maxsize)

usersPerToken = {}
indices = {}

#for c in ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']:
for c in ['5','6','7','8','9','a','b','c','d','e','f']:
    print("Letter", c)
    for i in range(8):
        print("\tBlock number", i)
        with open("../../ethereum_data/token_csvs/token_transfers%d.csv" % i) as csvfile: 
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0][0] == 't':
                    for i in range(len(row)):
                        indices[row[i]] = i
                else:
                    to = row[indices["token_address"]]
                    if to[2] != c:
                        continue
                    ta = row[indices["to_address"]]
                    fa = row[indices["from_address"]]
                    try:
                        usersPerToken[to].add(ta)
                    except KeyError:
                        usersPerToken[to] = set([ta])
                    try:
                        usersPerToken[to].add(fa)
                    except KeyError:
                        usersPerToken[to] = set([fa])
    
    with open("../../ethereum_data/usersPerToken/userAddressesPerToken%c.csv" % c, "w") as csvfile:
        for token in usersPerToken.keys():
            csvfile.write("%s,%s\n" % (token, '[' + ','.join(list(usersPerToken[token])) + ']'))
