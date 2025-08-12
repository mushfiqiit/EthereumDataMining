# findForkJoinAddress.csv
# Finds all the addresses that have only two transactions going in opposite
# directions in relation to the target address. These have to be with the 
# same token since the only way to have an outgoing edge of a given token is
# to have some of that token already

import csv

addressVal = {}

temporalWidth = 100

for filenum in range(20):
    print(filenum)
    with open("../../ethereum_data/token_csvs/token_transfers%02d.csv" % filenum) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            if row[0][0] == 't':
                indicies = {}
                for i in range(len(row)):
                    indicies[row[i]] = i
            else:
                ta = row[indicies["to_address"]]
                fa = row[indicies["from_address"]]
                bn = row[indicies["block_number"]]
                ta = int(ta, 0)
                fa = int(fa, 0)
                bn = int(bn)
                try:
                    if addressVal[ta] == 0.5:
                        addressVal[ta] = 0 # Too many transactions
                    elif addressVal[ta] > 0.9 and abs(bn - abs(addressVal[ta])) < temporalWidth:
                        addressVal[ta] = 0.5 # Valid
                    else:
                        addressVal[ta] = 0 # Too much time
                except KeyError:
                    addressVal[ta] = -bn
                try:
                    if addressVal[fa] == 0.5:
                        addressVal[fa] = 0 # Too many transactions
                    elif addressVal[fa] < -0.9 and abs(bn - abs(addressVal[fa])) < temporalWidth:
                        addressVal[fa] = 0.5 # Valid
                    else:
                        addressVal[fa] = 0 # Too much time
                except KeyError:
                    addressVal[fa] = bn

if temporalWidth > 1000000:
    with open("../../ethereum_data/forkJoin_nodes/forkJoinAddressAll.csv", 'w') as csvfile:
        for acc in addressVal.keys():
            if addressVal[acc] == 0.5:
                csvfile.write(hex(acc))
                csvfile.write("\n")
else:
    with open("../../ethereum_data/forkJoin_nodes/forkJoinAddressAll%dTime.csv" % temporalWidth, 'w') as csvfile:
        for acc in addressVal.keys():
            if addressVal[acc] == 0.5:
                csvfile.write(hex(acc))
                csvfile.write("\n")
