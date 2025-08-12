# findCsvGraphs.csv
# Takes data from all tokens and plots data relating to those transactions

import csv
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

dataPerAddress = {}
with open("../../ethereum_data/big_token_data.csv") as csvfile1:
    reader = csv.reader(csvfile1, delimiter=',', quotechar='|')
    for row in reader:
        if(row[0][0] == 'N'):
            N = len(row)
            indicies = list(np.repeat("",N))
            for j in range(N):
                row0 = row
        else:
            dataPerAddress[row[0]] = {}
            for i in range(1,N):
                try:
                    dataPerAddress[row[0]][row0[i]] = float(row[i])
                except ValueError:
                    dataPerAddress[row[0]][row0[i]] = row[i]

viralTokens = []
with open("../../ethereum_data/famousTokens.csv") as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in reader:
        viralTokens.append(row[0].lower())
viralTokens = set(viralTokens)

print("Data finished loading")

totalCount = 0
sizes = [500,5000,50000,500000,5000000,50000000]
sizeCounts = np.zeros_like(sizes)
for add in dataPerAddress.keys():
    totalCount += 1
    for i in range(len(sizes)):
        if dataPerAddress[add]["Count"] > sizes[i]:
            sizeCounts[i] += 1

fiveProps = []
fivePropsViral = []
counts = []
countsViral = []
thousandBlks = []
thousandBlksViral = []
for add in dataPerAddress.keys():
    fiveProps.append(dataPerAddress[add]["5% Proportion"])
    counts.append(dataPerAddress[add]["Count"])
    thousandBlks.append(dataPerAddress[add]["Within 1000 blocks"])
    if add in viralTokens:
        fivePropsViral.append(dataPerAddress[add]["5% Proportion"])
        countsViral.append(dataPerAddress[add]["Count"])
        thousandBlksViral.append(dataPerAddress[add]["Within 1000 blocks"])
    #if counts[-1] > 8e6:
        #print(add)
    if 2e4/counts[-1] < thousandBlks[-1]:
        print(add)

fig, ax = plt.subplots(1,1)
ax.loglog(sizes, sizeCounts)
fig.suptitle("Testing for a Scale Free Distribution")
ax.set_xlabel("Transaction Count")
ax.set_ylabel("Token Count")
plt.savefig("../ethereum_data/plots/scaleFreeSizes.png")
plt.clf()

fig, ax = plt.subplots(1,1)
ax.scatter(counts, fiveProps, marker='x', linewidths=1, color='blue')
ax.scatter(countsViral, fivePropsViral, marker='x', linewidths=1, color='orange')
ax.set_xscale('log')
ax.set_yscale('linear')
fig.suptitle("")
ax.set_xlabel("Transaction Count")
ax.set_ylabel("5% Proportion")
plt.savefig("../ethereum_data/plots/countToFivePercent.png")

fig, ax = plt.subplots(1,1)
ax.scatter(counts, thousandBlks, marker='x', linewidths=1, color='blue')
ax.scatter(countsViral, thousandBlksViral, marker='x', linewidths=1, color='orange')
x = np.geomspace(2e4,1e8,num=50)
ax.plot(x, 2e4*np.reciprocal(x), color='black')
ax.set_xscale('log')
ax.set_yscale('linear')
fig.suptitle("")
ax.set_xlabel("Transaction Count")
ax.set_ylabel("Within 1000 blocks")
plt.savefig("../ethereum_data/plots/countToThousandBlocks.png")

