import numpy as np
import csv
import sys

csv.field_size_limit(sys.maxsize)

tokenCounts = {}

for c in ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']:
    with open("../../ethereum_data/tokenPerAddress/tokensPerAddress%c.csv" % c) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            token = row[0]
            for address in row[1].split(";"):
                try:
                    tokenCounts[address] += 1
                except KeyError:
                    tokenCounts[address] = 1
    print("Part %c done" % c)

addresses = list(tokenCounts.keys())
addresses.sort(key = lambda z : -tokenCounts[z])

with open("../../ethereum_data/tokenValence.csv", "w") as csvfile:
    csvfile.write("address,count\n")
    for address in addresses:
        csvfile.write("%s,%d\n" % (address, tokenCounts[address]))
