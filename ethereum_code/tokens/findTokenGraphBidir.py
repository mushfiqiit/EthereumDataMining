# findTokenGraphBidir.py

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
    lastAmount = {}
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
                am = int(row[indicies["value"]])
                tbn = int(row[indicies["block_number"]])
                bn = (tbn // fidelity) * fidelity

                try:
                    lta = lastToken[fa][ta] # Check if there was a backwards arrow
                    lbn = lastBlock[fa][ta]
                    lam = lastAmount[fa][ta]
                    if abs(tbn - lbn) < temporalRange and fa != ta and lta != ad: # Self loops are bad
                        try:
                            tokenGraph[lta][ad][bn] = [sum(x) for x in zip(tokenGraph[lta][ad][bn], [1, lam, am])]
                        except KeyError:
                            try:
                                tokenGraph[lta][ad][bn] = [1, lam, am]
                            except KeyError:
                                try:
                                    tokenGraph[lta][ad] = {}
                                    tokenGraph[lta][ad][bn] = [1, lam, am]
                                except KeyError:
                                    tokenGraph[lta] = {}
                                    tokenGraph[lta][ad] = {}
                                    tokenGraph[lta][ad][bn] = [1, lam, am]
                except KeyError:
                    pass # IF there isn't, ignore the current pair

                try:
                    lastToken[ta][fa] = ad
                except KeyError:
                    lastToken[ta] = {}
                    lastToken[ta][fa] = ad
                try:
                    lastAmount[ta][fa] = am
                except KeyError:
                    lastAmount[ta] = {}
                    lastAmount[ta][fa] = am
                try:
                    lastBlock[ta][fa] = tbn
                except KeyError:
                    lastBlock[ta] = {}
                    lastBlock[ta][fa] = tbn

    if temporalRange < 1000000:
        with open("../../ethereum_data/token_graph/bidir/tokenGraph%dTime%02dBidir.csv" % (temporalRange, i), 'w') as csvfile:
            csvfile.write("Source,Target,Time,Weight,SourceAmount,TargetAmount\n")
            for fa in tokenGraph.keys():
                for ta in tokenGraph[fa].keys():
                    for bn in tokenGraph[fa][ta].keys():
                        wes = tokenGraph[fa][ta][bn]
                        we = wes[0]
                        sam = wes[1] # Source amount
                        tam = wes[2] # Target amount
                        csvfile.write("%s,%s,%d,%d,%d,%d\n" % (str(hex(fa)),str(hex(ta)),bn,we,sam,tam))
    else:
        with open("../../ethereum_data/token_graph/bidir/tokenGraph%02dBidir.csv" %i, 'w') as csvfile:
            csvfile.write("Source,Target,Time,Weight,SourceAmount,TargetAmount\n")
            for fa in tokenGraph.keys():
                for ta in tokenGraph[fa].keys():
                    for bn in tokenGraph[fa][ta].keys():
                        wes = tokenGraph[fa][ta][bn]
                        we = wes[0]
                        sam = wes[1] # Source amount
                        tam = wes[2] # Target amount
                        csvfile.write("%s,%s,%d,%d,%d,%d\n" % (str(hex(fa)),str(hex(ta)),bn,we,sam,tam))
