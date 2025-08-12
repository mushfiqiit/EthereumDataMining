# findTokenGraph2.py

import csv
import numpy as np

multiTransaction = set()
with open("../../ethereum_data/multiTransactions.py") as readfile:
    reader = csv.reader(readfile)
    for row in reader:
        th = int(row[0], 0)
        multiTransaction.add(th)

for fji in range(20):
    transactionToFJNodes = {}

    print(fji)

    with open('../../ethereum_data/token_csvs/token_transfers%02d.csv' % fji) as csvfile2:
            reader2 = csv.reader(csvfile2)

            for row in reader2:
                if row[0][0] != '0':
                    indicies = {}
                    for i in range(len(row)):
                        indicies[row[i]] = i
                else:
                    th = int(row[indicies["transaction_hash"]], 0)
                    to = int(row[indicies["token_address"]], 0)
                    ta = int(row[indicies["to_address"]], 0)
                    fa = int(row[indicies["from_address"]], 0)
                    bn = int(row[indicies["block_number"]])
                    if th not in multiTransaction:
                        continue
                    try:
                        transactionToFJNodes[th].add((to,ta,fa,bn))
                    except KeyError:
                        transactionToFJNodes[th] = set([(to,ta,fa,bn)])

    #for th in transactionToFJNodes.keys():
    #    if len(transactionToFJNodes[th]) > 1:
    #        print(th)
    #        print(transactionToFJNodes[th])
    with open('../../ethereum_data/token_graph/tokenGraph2%02dSame.csv' % fji, 'w') as writefile:
        writer = csv.writer(writefile)
        writer.writerow(["Label", "Id", "Weight", "Time"])
        for th in transactionToFJNodes.keys():
            tokens = [el[0] for el in transactionToFJNodes[th]]
            times = [el[3] for el in transactionToFJNodes[th]]
            bn = times[0]
            if all(tokens[0] == token for token in tokens):
                writer.writerow([hex(tokens[0]), hex(tokens[0]), len(tokens), str(bn)])
