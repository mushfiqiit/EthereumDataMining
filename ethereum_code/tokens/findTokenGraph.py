# findTokenGraph.py
# Find the graphs between the tokens, where edges are represented
# by neighboring transactions of tokens of differeing tokens

import csv
import numpy as np

tokensPerAddress = {}

temporalRange = 250

# HOURS
fidelity = 250
# DAYS
#fidelity = 6000
# WEEKS
#fidelity = 42000
# MONTHS 
#fidelity = 180000

for i in range(20):
    lastBlock = {}
    tokenGraph = {}
    lastToken = {}
    lastDirOut = {}
    print("Block number %d" % i)
    with open("../../ethereum_data/token_csvs/token_transfers%02d.csv" % i) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            if row[0][0] == 't':
                indicies = {}
                for j in range(len(row)):
                    indicies[row[j]] = j
            else:
                ta = int(row[indicies["to_address"]], 0)
                fa = int(row[indicies["from_address"]], 0)
                ad = int(row[indicies["token_address"]], 0)
                tbn = int(row[indicies["block_number"]])
                bn = (tbn // fidelity) * fidelity

                try:
                    lta = lastToken[ta]
                    if lastDirOut[ta] == True and abs(tbn - lastBlock[ta]) < temporalRange:
                        try:
                            tokenGraph[lta][ad][bn] += 1
                        except KeyError:
                            try:
                                tokenGraph[lta][ad][bn] = 1
                            except KeyError:
                                try:
                                    tokenGraph[lta][ad] = {}
                                    tokenGraph[lta][ad][bn] = 1
                                except KeyError:
                                    tokenGraph[lta] = {}
                                    tokenGraph[lta][ad] = {}
                                    tokenGraph[lta][ad][bn] = 1
                except KeyError:
                    pass
                try:
                    lta = lastToken[fa]
                    if lastDirOut[fa] == False and abs(tbn - lastBlock[fa]) < temporalRange:
                        try:
                            tokenGraph[lta][ad][bn] += 1
                        except KeyError:
                            try:
                                tokenGraph[lta][ad][bn] = 1
                            except KeyError:
                                try:
                                    tokenGraph[lta][ad] = {}
                                    tokenGraph[lta][ad][bn] = 1
                                except KeyError:
                                    tokenGraph[lta] = {}
                                    tokenGraph[lta][ad] = {}
                                    tokenGraph[lta][ad][bn] = 1
                except KeyError:
                    pass

                lastToken[ta] = ad
                lastDirOut[ta] = False
                lastBlock[ta] = tbn
                lastToken[fa] = ad
                lastDirOut[fa] = True
                lastBlock[fa] = tbn

    if temporalRange < 1000000:
        with open("../../ethereum_data/token_graph/tokenGraph%dTime%02d.csv" % (temporalRange, i), 'w') as csvfile:
            csvfile.write("from_address,to_address,Time,Weight\n")
            for fa in tokenGraph.keys():
                for ta in tokenGraph[fa].keys():
                    for bn in tokenGraph[fa][ta].keys():
                        we = tokenGraph[fa][ta][bn]
                        csvfile.write("%s,%s,%d,%d\n" % (str(hex(fa)),str(hex(ta)),bn,we))
    else:
        with open("../../ethereum_data/token_graph/tokenGraph%02d.csv" %i, 'w') as csvfile:
            csvfile.write("from_address,to_address,Time,Weight\n")
            for fa in tokenGraph.keys():
                for ta in tokenGraph[fa].keys():
                    for bn in tokenGraph[fa][ta].keys():
                        we = tokenGraph[fa][ta][bn]
                        csvfile.write("%s,%s,%d,%d\n" % (str(hex(fa)),str(hex(ta)),bn,we))
