# findTokenGraphLimited.py

import csv
import numpy as np

tokens = []
with open("../../ethereum_data/token_freq.csv") as readfile:
    reader = csv.reader(readfile)
    for row in reader:
        if row[0] == "":
            indices = {}
            for i in range(len(row)):
                indices[row[i]] = i
        else:
            if int(row[indices['freq']]) > 100000: # Arbitrary cut off
                tokens.append(row[indices['token']])

tokens = set(tokens)
for index in range(20):
    print(index)
    with open("../../ethereum_data/token_graph/tokenGraph250Time%02d.csv" % index) as readfile:
        with open("../../ethereum_data/token_graph/tokenGraph250TimeLimited%02d.csv" % index, 'w') as writefile:
            reader = csv.reader(readfile)
            writer = csv.writer(writefile)
            for row in reader:
                if row[0] == "from_address":
                    writer.writerow(["Source","Target","Time","Weight"])
                    indices = {}
                    for i in range(len(row)):
                        indices[row[i]] = i
                else:
                    fa = row[indices["from_address"]]
                    ta = row[indices["to_address"]]
                    if fa in tokens and ta in tokens:
                        if fa != ta: # Get rid of self loops
                            writer.writerow(row)
