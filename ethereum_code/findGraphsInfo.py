# findGraphsInfo.py
# Finds a lot of properties about the tokens with a relatively high 
# transaction count. Most notably, this makes a movie of the 
# density of fork-join nodes in the entire Ethereum ecosystem

import numpy as np
import matplotlib.animation as animation
import csv
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def dist(x1, y1, x2, y2):
    x = (x2-x1)
    y = (y2-y1)
    return x*x+y*y

def findClosest(xs, ys, xsearch, ysearch, names):
    m = 100000000
    maxX = max(xs)
    minX = min(xs)
    maxY = max(ys)
    minY = min(ys)
    tX = maxX-minX
    tY = maxY-minY
    d = np.zeros(len(xs))
    for i in range(len(xs)):
        d[i] = dist((xs[i]-minX)/tX, (ys[i]-minY)/tY, (xsearch-minX)/tX, (ysearch-minY)/tY)
    idx = np.argpartition(d, 5)
    names = np.copy(names)
    return names[idx[:5]]

# Get the more notable tokens
tokens = []
with open('../ethereum_data/token_csvs_big_filenames.csv') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        tokens = row
        break

# Finds the number of transaction for the 'big' tokens
counts = {}
with open("../ethereum_data/big_token_data.csv") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        try:
            if row[0][0] == 'N':
                indicies = {}
                for i, elem in enumerate(row):
                    indicies[elem] = i
            else:
                t = row[indicies["Name"]]
                c = int(row[indicies["Count"]])
                counts[t] = c
        except Exception:
            pass

names = []
xs = []
xs2 = []
ys = []
modeUserInFirst500 = []
blocksTo500 = []
fidelity = 25000
maxBlock = 16000000
timesPerToken = np.zeros((len(tokens)-1, int(maxBlock/fidelity)))
countsPerToken = np.zeros((len(tokens)-1, int(maxBlock/fidelity)))
tokenIndex = -1
for tokenFile in tokens:
    tokenIndex += 1
    token = tokenFile[:-4]
    addresses = set([])
    lastTransferTime = {}
    firstTransferTime = {}
    addresses500 = set([])
    transfersInFirst500PerAddress = {}
    addressMoreThanOnce = set([])
    addressMoreThanTwice = set([])
    names.append(token)
    try:
        with open("../ethereum_data/token_csvs_big/%s.csv" % token) as csvfile:
            reader = csv.reader(csvfile)
            i = -1
            for row in reader:
                i += 1
                try:
                    if row[0][0] == 't':
                        indicies = {}
                        for j in range(len(row)):
                            indicies[row[j]] = j
                    else:
                        fa = row[indicies["from_address"]]
                        ta = row[indicies["to_address"]]
                        ti = int(row[indicies["block_number"]])
                        if fa in addressMoreThanOnce:
                            addressMoreThanTwice.add(fa)
                        elif fa in addresses:
                            addressMoreThanOnce.add(fa)
                        else:
                            firstTransferTime[fa] = ti
                        if ta in addressMoreThanOnce:
                            addressMoreThanTwice.add(ta)
                        elif ta in addresses:
                            addressMoreThanOnce.add(ta)
                        else:
                            firstTransferTime[ta] = ti
                        addresses.add(fa)
                        addresses.add(ta)
                        lastTransferTime[fa] = ti
                        lastTransferTime[ta] = ti

                        if i == 1:
                            block1 = ti
                        if i == 500:
                            block500 = ti
                        if i < 500:
                            addresses500.add(fa)
                            addresses500.add(ta)
                            try:
                                transfersInFirst500PerAddress[fa] += 1
                            except KeyError:
                                transfersInFirst500PerAddress[fa] = 1
                            try:
                                transfersInFirst500PerAddress[ta] += 1
                            except KeyError:
                                transfersInFirst500PerAddress[ta] = 1
                except Exception:
                    pass
    except Exception:
        continue
    addresses = list(addresses)
    addressesMoreThanOnce = list(addressMoreThanOnce)
    addressesMoreThanTwice = list(addressMoreThanTwice)
    print(token,"  %4d   %4d  %4d" % (len(addresses), counts[token], len(addressMoreThanTwice)))
    xs.append(len(list(addresses500)))
    if len(addresses) == 0:
        xs2.append(0)
    else:
        xs2.append((len(addressMoreThanOnce) - len(addressMoreThanTwice)) / len(addresses))
        for tok in addressMoreThanOnce:
            if tok not in addressMoreThanTwice:
                timesPerToken[tokenIndex][(int(lastTransferTime[tok]/fidelity)):] += 1
        for tok in addresses:
            countsPerToken[tokenIndex][(int(firstTransferTime[tok]/fidelity)):] += 1
        for t in range(int(maxBlock/fidelity)):
            if countsPerToken[tokenIndex][t] != 0:
                timesPerToken[tokenIndex][t] /= countsPerToken[tokenIndex][t]
            else:
                countsPerToken[tokenIndex][t] = 0.1
    maxAddress = max(transfersInFirst500PerAddress.keys(), key = lambda z : transfersInFirst500PerAddress[z])
    transfersInFirst500PerAddress[maxAddress] = 0
    maxAddress = max(transfersInFirst500PerAddress.keys(), key = lambda z : transfersInFirst500PerAddress[z])
    modeUserInFirst500.append(transfersInFirst500PerAddress[maxAddress])
    blocksTo500.append(block500-block1)
    ys.append(counts[token])

#def animate(frame_number):
#    x = np.linspace(0, 4, 1000)
#    y = np.sin(2 * np.pi * (x - 0.01 * frame_number))
#    line.set_data(x, y)
#    line.set_color('green')
#    return line,

#fig, ax = plt.subplots()
#anim = animation.FuncAnimation(fig, animate, frames=1000, 
#                               interval=20, blit=True)
#fig.suptitle('Straight Line plot', fontsize=14)
  
#writervideo = animation.FFMpegWriter(fps=60)
#anim.save('forkJoinsOverTime.mp4', writer=writervideo)

pd.DataFrame(timesPerToken).to_csv("../ethereum_data/timesPerToken.csv")
pd.DataFrame(np.log10(countsPerToken)).to_csv("../ethereum_data/countsPerToken.csv")
np.savetxt('tokenNames.csv', [names], delimiter=',', fmt='%s')

fig, ax = plt.subplots()
moviewriter = animation.FFMpegWriter(fps=30)
with moviewriter.saving(fig, '../ethereum_data/plots/forkJoinsOverTime.mp4', dpi=100):
  for j in range(int(maxBlock/fidelity)):
    if all(countsPerToken[:,j] == 1):
      continue
    try:
      sns.kdeplot(x=timesPerToken[:,j], y=np.log10(countsPerToken[:,j]), shade=True, thresh=0)
    except ValueError:
      print("Value Error")
      plt.clf()
    #plt.colorbar(ax.get_children()[2], ax)
    #sns.kdeplot(x=timesPerToken[:,j], y=np.log10(countsPerToken[:,j]), shade=True, cbar=True)
    plt.title("Time - %d" % int(j*maxBlock/fidelity))
    plt.xlabel("Fork-Join Ratio")
    plt.ylabel("$log(n)$")
    plt.xlim([0, 1])
    plt.ylim([0, 8.5])
    moviewriter.grab_frame()

#plt.clf()
#plt.hist(timesArray, bins=200)
#plt.xlabel("Block Number")
#plt.xlim([0, 500])
#plt.ylabel("Fork-Join Count")
#plt.title("Fork Join Nodes Over Time")
#plt.savefig("../ethereum_data/plots/forkJoinOverTime.png")

plt.clf()
sns.kdeplot(x=xs, y=np.log10(ys), cmap="Blues", shade=True, thresh=0)
plt.xlabel("Unique Address")
plt.xlim([0, 500])
plt.ylabel("$log(n)$")
plt.title("Comparing Unique number of Addresses to Count per Token")
plt.savefig("../ethereum_data/plots/uniqueInFirst500.png")
df = pd.DataFrame({'Names':names[:30406], 'Unique Addresses':xs[:30406], 'LogCount': np.log10(ys)[:30406]})
df.to_csv("../ethereum_data/plots/uniqueInFirst500.csv", header=True, index=False)

plt.clf()
sns.kdeplot(x=xs2, y=np.log10(ys), cmap="Blues", shade=True, thresh=0)
plt.title("Comparing Fork-Join ratios to Transaction Count per Token")
plt.xlabel("Ratio of Fork Join Nodes")
plt.ylabel("$log(n)$")
plt.savefig("../ethereum_data/plots/forkJoinRatio.png")
df = pd.DataFrame({'Names':names[:30406], 'Fork-Join Ratio':xs2[:30406], 'LogCount': np.log10(ys)[:30406]})
df.to_csv("../ethereum_data/plots/forkJoinRatio.csv", header=True, index=False)

plt.clf()
sns.kdeplot(x=blocksTo500, y=np.log10(ys), cmap="Blues", shade=True, thresh=0)
plt.title("Comparing Time to 500 Transactions to Transaction Count per Token")
plt.xlabel("Blocks to 500 Transactions")
plt.ylabel("$log(n)$")
plt.savefig("../ethereum_data/plots/timeTo500.png")
df = pd.DataFrame({'Names':names[:30406], 'Time to 500 Transactions':blocksTo500[:30406], 'LogCount': np.log10(ys)[:30406]})
df.to_csv("../ethereum_data/plots/timeTo500.csv", header=True, index=False)

plt.clf()
sns.kdeplot(x=modeUserInFirst500, y=np.log10(ys), cmap="Blues", shade=True, thresh=0)
plt.title("Comparing 2nd Mode User to Transaction Count per Token")
plt.xlabel("Mode User in First 500")
plt.ylabel("$log(n)$")
plt.savefig("../ethereum_data/plots/mode500snd.png")
df = pd.DataFrame({'Names':names[:30406], 'Second Mode User':modeUserInFirst500[:30406], 'LogCount': np.log10(ys)[:30406]})
df.to_csv("../ethereum_data/plots/mode500snd.csv", header=True, index=False)

# This section is for finding the data of specific nodes by approximating the
# position of the node and then finding the closest point
print("Mode for unique in 500: ", findClosest(xs, np.log10(ys), 140, 2.9, names))
print("Second mode for unique in 500: ", findClosest(xs, np.log10(ys), 480, 3.2, names))
print("Third mode for unique in 500: ", findClosest(xs, np.log10(ys), 480, 3.9, names))

print("Fork Join Bottom Left: ", findClosest(xs2, np.log10(ys), 0.0, 2.8, names))
print("Fork Join Bottom Right: ", findClosest(xs2, np.log10(ys), 0.45, 2.8, names))
print("Fork Join Top Left: ", findClosest(xs2, np.log10(ys), 0.0, 4.2, names))
print("Fork Join Top Right: ", findClosest(xs2, np.log10(ys), 0.4, 4.5, names))
