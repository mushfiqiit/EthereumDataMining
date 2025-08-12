import matplotlib.pyplot as plt
import numpy as np
import random
import csv

indices = {}
x = []
y = []
with open("../ethereum_data/uni_transactions.csv") as readfile:
    reader = csv.reader(readfile)
    for row in reader:
        if row[0] == 'timestamp':
            indices = {}
            for i in range(len(row)):
                indices[row[i]] = i
        elif float(row[indices['token_value']]) != 0:
            ratio = float(row[indices['ether_value']])/float(row[indices['token_value']])
            if ratio < 0.05:
                #x.append(int(row[indices['timestamp']]))
                x.append(int(row[indices['block_number']]))
                y.append(ratio)

both = list(zip(x,y))
both.sort(key = lambda z: z[0])
#print(both)
xx, yy = zip(*both)
xx = list(xx)
yy = list(yy)

width = 1000
tolerance = 0.03

x = [xx[0]]
y = [yy[0]]
for i in range(1,len(xx)):
    if i % 100 == 99:
        print(xx[i], med)
    if i >= width:
        med = np.median(yy[i-width:i])
        #std = np.std(yy[i-width:i])
        std = tolerance * med
    else:
        med = np.median(yy[:i])
        #std = np.std(yy[:i])
        std = tolerance * med
    if med - 2 * std < yy[i] and yy[i] < med + 2 * std:
        x.append(xx[i])
        y.append(yy[i])

x = np.array(x)
y = np.array(y)

#indices = np.arange(0, len(x), 1+int(len(x)/2000))
indices = np.arange(0, len(x))
#plt.scatter(x=x[randomIndices], y=y[randomIndices], marker='.')
plt.plot(x[indices], y[indices], marker=',')
plt.xlabel("Timestamp")
plt.ylabel("Ether Cost")
plt.title("Sample transaction prices of Uniswap overtime")

plt.savefig("../ethereum_data/uni_transactions.png")
