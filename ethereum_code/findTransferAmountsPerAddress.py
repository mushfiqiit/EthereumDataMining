# findTransferAmountsPerToken.py
# Finding the total valence of users

import csv

counts = {}
for index in range(8):
    with open("../ethereum_data/token_csvs/token_transfers%d.csv" % index, 'r') as csvfile:
        print("Working on file %d" % index)
        reader = csv.reader(csvfile, delimiter=",", quotechar="|")
        for row in reader:
            if row[0] == "token_address":
                indicies = {}
                for i in range(len(row)):
                    indicies[row[i]] = i
            else:
                ta = row[indicies["to_address"]]
                fa = row[indicies["from_address"]]
                if ta not in counts.keys():
                    counts[ta] = 0
                if fa not in counts.keys():
                    counts[fa] = 0
                counts[ta] += 1
                counts[fa] += 1

arr = []
for acc in counts.keys():
    arr.append((acc, counts[acc]))
arr.sort(key = lambda y: -y[1])

with open("../ethereum_data/transferCounts.csv", 'w', newline='') as csvfile:
    csvfile.write("Account, Number of Transfers\n")
    for elem in arr:
        csvfile.write("%s, %d\n" % elem)
