# findForkJoinGraph.py
# Restricts the full transaction network to only the transactions that 
# are fork join, or at least seems like it (since it only looks at some
# of the network at a time, split up by time)

import csv
import numpy as np

timeRes = False

fjNodes = set([])
if timeRes:
    with open("../../ethereum_data/forkJoin_nodes/forkJoinAddressAll100Time.csv") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            fjNodes.add(row[0])
else:
    with open("../../ethereum_data/forkJoin_nodes/forkJoinAddressAll.csv") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            fjNodes.add(row[0])

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
                    th = row[indicies["transaction_hash"]]
                    to = row[indicies["token_address"]]
                    ta = row[indicies["to_address"]]
                    fa = row[indicies["from_address"]]
                    bn = row[indicies["block_number"]]
                    if fa in fjNodes or ta in fjNodes:
                        try:
                            transactionToFJNodes[th].add((to,ta,fa,bn))
                        except KeyError:
                            transactionToFJNodes[th] = set([(to,ta,fa,bn)])

    #for th in transactionToFJNodes.keys():
    #    if len(transactionToFJNodes[th]) > 1:
    #        print(th)
    #        print(transactionToFJNodes[th])
    with open('../../ethereum_data/token_graph/forkJoin_graph/forkJoinGraph2%02d.csv' % fji, 'w') as writefile:
        writer = csv.writer(writefile)
        writer.writerow(["Source", "Target", "Time"])
        for th in transactionToFJNodes.keys():
            tokens = [el[0] for el in transactionToFJNodes[th]]
            times = [el[3] for el in transactionToFJNodes[th]]
            bn = times[0]
            for i in range(len(tokens)-1):
                for j in range(i+1, len(tokens)):
                    if tokens[i] != tokens[j]:
                        writer.writerow([tokens[i], tokens[j], bn])
