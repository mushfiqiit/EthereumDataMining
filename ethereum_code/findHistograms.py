# findHistograms.py
# This finds the transactions overtime for high-transacting tokens
# and saves that data into a csv to be ploted in histograms later

import csv
import numpy as np

thres = 2000
fidelity = 200000
startblock = 0
endblock = 14000000

hists = {}
addresses = []
with open("../ethereum_data/transferCounts.csv") as csvfile1:
    reader = csv.reader(csvfile1, delimiter=',', quotechar='|')
    for row in reader:
        if(int(row[1]) > thres):
            hists[row[0]] = np.zeros(((endblock-startblock)//fidelity)+1)
            addresses.append(row[0])
        else:
            break

addresses = set(addresses)
for i in range(7):
    print("Working on file %d" % i)
    with open("../ethereum_data/token_csvs/token_transfers%d.csv" % i) as csvfile1:
        reader = csv.reader(csvfile1, delimiter = ',', quotechar = '|')
        for row in reader:
            if row[0] == "token_address":
                indicies = {}
                for j in range(len(row)):
                    indicies[row[j]] = j
            else:
                bn = int(row[indicies["block_number"]])
                if bn < startblock or endblock < bn:
                    continue
                index = (bn - startblock) // fidelity
                ta = row[indicies["to_address"]]
                fa = row[indicies["from_address"]]
                if ta in addresses:
                    hists[ta][index] = hists[ta][index] + 1
                if fa in addresses:
                    hists[fa][index] = hists[fa][index] + 1

with open("../ethereum_data/hists.csv", 'w', newline = '') as csvfile1:
    csvfile1.write("time")
    ran = ((endblock-startblock)//fidelity)+1
    for i in range(ran):
        csvfile1.write(", %d" % (startblock + i*fidelity))
    csvfile1.write("\n")
    for add in hists.keys():
        csvfile1.write(add)
        for i in range(ran):    
            csvfile1.write(", %d" % hists[add][i])
        csvfile1.write("\n")
