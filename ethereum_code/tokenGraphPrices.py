import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import numpy.ma as ma
import heapq
import time
import datetime
import csv

masked = True
fixAnomolyPrices = True
fixStationary = True
#threshold = 0.99
threshold = 0.6
#threshold = 1 # Log threshold

blockTimes = []
with open("blockTimes.csv") as readfile:
    reader = csv.reader(readfile)
    for row in reader:
        bn = int(row[0])
        ti = int(row[1])
        if bn % 100 == 0 and bn > 1000000:
            blockTimes.append((bn,ti))
blockTimes.sort(key = lambda z: z[0])

def timeInRange(t):
    return t > blockTimes[0][1]

def getTimeBlock(t):
    i = 0
    while i < len(blockTimes) and t > blockTimes[i][1]:
        i += 1
    if i <= 0:
        return blockTimes[0][0]
    if i == len(blockTimes):
        return blockTimes[-1][0]
    startTime = blockTimes[i][1]
    endTime = blockTimes[i+1][1]
    startBlock = blockTimes[i][0]
    endBlock = blockTimes[i+1][0]
    # a*(t-c)+b
    if startTime == endTime:
        return startBlock
    a = (endBlock-startBlock)/(endTime-startTime)
    b = startBlock
    c = startTime
    return a*(t-c) + b

currencies = pd.read_csv("currency_prices.csv", header=None)
timestemp = currencies.iloc[9:,0].values
times = []
for t in timestemp:
    if int(t.split('-')[0]) < 1970:
        continue
    temp = time.mktime(datetime.datetime.strptime(t, "%Y-%m-%d").timetuple())
    if timeInRange(temp):
        times.append(getTimeBlock(temp))

currencies = pd.DataFrame(currencies.iloc[-len(times):,1:].values, columns=currencies.loc[2,1:].values, index=times)
currencies = currencies.loc[:,~currencies.columns.duplicated()].copy()
print(currencies.columns)
currencies.drop(['VEF:Bolivar'], axis=1, inplace=True)
currencies.fillna(-100000, inplace=True)

#currencies = pd.DataFrame()
print(currencies)

df = pd.DataFrame()
for fileindex in range(20):
    print(fileindex)
    filename = "tokenGraph/bidir/tokenGraph250Time%02dBidir.csv" % fileindex

    tempdf = pd.read_csv(filename, dtype={'Source': str, 'Target': str, 'Time': int, 'Weight': int, 'SourceAmount': float, 'TargetAmount': float}).dropna()
    df = df.append(tempdf)

edges = list(set(list(zip(df['Source'].values, df['Target'].values))))

print(df)

edgedict = {}
reversedict = {}
times = {}
valence = {}
sidedvalence = {}

for currency in currencies.columns:
    valence[currency.lower()] = 10000000
    sidedvalence[currency.lower()] = 10000000

# [Source][Target] = [(Time, SourceAmount, TargetAmount)]
for row in df.values:
    if float(row[4]) == 0 or float(row[5]) == 0:
        continue
    try:
        times[row[0]].append(int(row[2]))
    except KeyError:
        times[row[0]] = [int(row[2])]
    if row[0] != row[1]:
        try:
            times[row[1]].append(int(row[2]))
        except KeyError:
            times[row[1]] = [int(row[2])]
    try:
        edgedict[row[0]][row[1]].append((row[2],row[4],row[5]))
    except KeyError:
        try:
            edgedict[row[0]][row[1]] = []
            edgedict[row[0]][row[1]].append((row[2],row[4],row[5]))
        except KeyError:
            edgedict[row[0]] = {}
            edgedict[row[0]][row[1]] = []
            edgedict[row[0]][row[1]].append((row[2],row[4],row[5]))

    try:
        reversedict[row[1]][row[0]].append((row[2],row[4],row[5]))
    except KeyError:
        try:
            reversedict[row[1]][row[0]] = []
            reversedict[row[1]][row[0]].append((row[2],row[4],row[5]))
        except KeyError:
            reversedict[row[1]] = {}
            reversedict[row[1]][row[0]] = []
            reversedict[row[1]][row[0]].append((row[2],row[4],row[5]))

starttime = {}
endtime = {}
for token in times.keys():
    starttime[token] = min(times[token])
    endtime[token] = max(times[token])
tokenmin = min(starttime.values())
tokenmax = max(endtime.values())
currmin = min(currencies.index)
currmax = max(currencies.index)
for currency in currencies.columns:
    starttime[currency.lower()] = min([tokenmin,currmin])
    endtime[currency.lower()] = max([tokenmax,currmax])

vals = set()
vals.update(list(edgedict.keys()))
    
for val in vals:
    sidedvalence[val] = 0
    for val2 in edgedict[val].keys():
        sidedvalence[val] += len(edgedict[val][val2]) 
    
vals = set()
vals.update(list(reversedict.keys()))
vals.update(list(edgedict.keys()))

for val in vals:
    valence[val] = 0
    if val in edgedict.keys():
        for val2 in edgedict[val].keys():
            valence[val] += len(edgedict[val][val2]) 
    if val in reversedict.keys():
        for val2 in reversedict[val].keys():
            valence[val] += len(reversedict[val][val2])

#valence = sidedvalence

def getPrice(token, time):
    if token not in pricedict.keys():
        raise Exception("Token not in the price dict yet (somehow)")
    if len(pricedict[token]) == 0:
        print("No price data for", token)
        return np.NaN
    # If before the first transaction of the token, make price 0 (invalid)
    if time < starttime[token]:
        if masked:
            return np.NaN
        else:
            return 0
    index = -1
    maxindex = len(pricedict[token])-1
    # Find previous price 
    for i, (t,price) in enumerate(pricedict[token]):
        if t > time:
            break
        index = i
    # If there is no previous price, but there was some transaction, make the price the earliest known price
    if index == -1:
        return pricedict[token][0][1]
        # return 0
    # If there is no later price, return the last seen price
    elif index == maxindex:
        return pricedict[token][-1][1]
        #return 0
    # Otherwise, linearly interpolate between neighboring prices
    else:
        slope = (pricedict[token][index+1][1]-pricedict[token][index][1])/(pricedict[token][index+1][0]-pricedict[token][index][0])
        return slope*(time-pricedict[token][index][0])+pricedict[token][index][1]

startToken = '0xdAC17F958D2ee523a2206206994597C13D831ec7'
startToken = startToken.lower()

pricedict = {}

for c in currencies.columns:
    currency = c.lower()
    pricedict[currency] = []
    #values = currencies.loc[:,currency].values
    values = currencies[c].values
    print(values)
    indexs = currencies[c].index
    for i in range(len(values)):
        if values[i] >= 0 and indexs[i] >= 7000000 and indexs[i] < 15050000:
            pricedict[currency].append((indexs[i], values[i]))

for c in currencies.columns:
    currency = c.lower()
    print(list(map(lambda x: x[1], pricedict[currency])))

# [Token] = [(Time,Price)]
pricedict[startToken] = [(df['Time'].min(),1),(df['Time'].max(),1)]
processQueue = []
heapq.heappush(processQueue, (-valence[startToken], startToken))

while len(processQueue) > 0:
    (v, token) = heapq.heappop(processQueue)
    if token not in edgedict.keys():
        continue
    for neighbor in edgedict[token].keys():
        if neighbor in pricedict.keys():
            continue
        # else - no prices yet
        pricedict[neighbor] = []
        for (time,sa,ta) in edgedict[token][neighbor]:
            if float(ta) == 0:
                print("Edge weight of", ta, "between", token, "and", neighbor)
                continue
            price = abs(float(getPrice(token,time)) * float(sa) / float(ta))
            #price = float(ta) / (float(sa) * float(getPrice(token,time)))
            pricedict[neighbor].append((time,price))
        if len(pricedict[neighbor]) == 0:
            pricedict.pop(neighbor)
            continue
        heapq.heappush(processQueue, (-valence[neighbor], neighbor))

if fixAnomolyPrices:
    for token in pricedict.keys():
        print(token)
        pricelist = pricedict[token]

        xst = [z[0] for z in pricelist]
        yst = [z[1] for z in pricelist]

        #while len(yst) >= 2 and yst[1] > yst[0]: # Wait until the price goes down
        #    xst = xst[1:]
        #    yst = yst[1:]

        if len(xst) <= 1:
            continue

        xs, ys = [], []
        width = 0.02
        #window = (1/np.sqrt(len(xst))) * (np.max(xst) - np.min(xst))
        window = (2/np.sqrt(len(xst))) * (np.max(xst) - np.min(xst))
        minind = 0
        maxind = 1
        for i in range(len(xst)):
            #print(len(xst))
            #print(xst[maxind])
            while maxind < len(xst)-1 and xst[maxind] < xst[i] + window:
                maxind += 1
            while minind < maxind-1 and minind < len(xst)-2 and xst[minind] < xst[i] - window:
                minind += 1
            """
            lowlim = np.quantile(yst[minind:maxind], 0.5-width)
            uplim = np.quantile(yst[minind:maxind], 0.5+width)
            if lowlim <= yst[i] and yst[i] <= uplim:
                xs.append(xst[i])
                ys.append(float(yst[i]))
            """
            xs.append(xst[i])
            ys.append(np.median(yst[minind:maxind]))
            #"""
    
        if len(ys) == 0:
            print("Issue with token", token)
            continue

        pricedict[token] = list(zip(xs, ys))
    print("Done fixing anomaly prices")

if fixStationary:
    for token in pricedict.keys():
        prices = pricedict[token]
        sumx, sumy, count, product, sqrx = 0,0,0,0,0
        for (x,y) in prices:
            sumx += x
            sumy += y
            count += 1
        sumx /= count
        sumy /= count
        for (x,y) in prices:
            product += (x-sumx)*(y-sumy)
            sqrx += (x-sumx)*(x-sumx)
        if sqrx == 0:
            continue
        beta = product / sqrx
        alpha = sumy - (beta * sumx)

        newprices = []
        for (x,y) in prices:
            newprices.append((x,y-beta*x - alpha))
        pricedict[token] = newprices

print("Test")
print(list(filter(lambda z: z[0] != '0', list(pricedict.keys()))))
print("Test")

#testToken = '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2' # WETH
testTokens = []
for token in valence.keys():
    if valence[token] > 5000000 and token in pricedict.keys():
        testTokens.append(token)
#testTokens.append('0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984') # UNI
#testTokens.append('') # 
testTokens = [testToken.lower() for testToken in testTokens]
print(testTokens)
print("Test Tokens")

# CORRELATIONS
def corr(tokens):
    print("Running corr for %d tokens" % len(tokens))
    tokVals = np.array([])
    tokTimes = []
    for token in tokens:
        tok = pricedict[token]    
        tokTimes = tokTimes + [t for (t,a) in tok]

    print("Tokens are done")
    
    #"""
    mintime = min(tokTimes)
    maxtime = max(tokTimes)
    xs = np.linspace(mintime, maxtime, 1200)
    """
    # xs = tokTimes
    # xs.sort()
    """

    tokVals = []
    for token in tokens:
        ys = [getPrice(token, x) for x in xs]
        if len(tokVals) == 0:
            tokVals = ys
        else:
            tokVals = np.vstack([tokVals, ys]) 
    #tokVals = tokVals.T

    if masked:
        #mat = ma.corrcoef(ma.masked_invalid(tokVals[:len(xs)]))
        mat = ma.corrcoef(ma.masked_invalid(tokVals))
        mat = np.nan_to_num(mat)
        print(mat)
        return mat
    else:
        return np.corrcoef(tokVals)

def corr2(tokens):
    print("Finding Correlation")
    tokTimes = [] # This is only for a full-time correlation
    for token in tokens:
        tokTimes = tokTimes + [t for (t,a) in pricedict[token]]
    startTime = min(tokTimes)
    endTime = max(tokTimes)

    corrcoef = np.eye(len(tokens))
    for i in range(len(tokens)):
        for j in range(i+1, len(tokens)):
            print(i,j)
            tokiTimes = [t for (t,a) in pricedict[tokens[i]]]
            tokjTimes = [t for (t,a) in pricedict[tokens[j]]]
            tokTimes = np.array(tokiTimes + tokjTimes)
            firstTime = max([min(tokiTimes), min(tokjTimes)])
            lastTime = min([max(tokiTimes), max(tokjTimes)])
            times = len(tokTimes)
            times2 = np.sum([a and b for (a, b) in zip(tokTimes >= firstTime, tokTimes <= lastTime)])
            print(times2)
            if times2 < 100:
                continue
            #newtimes = np.linspace(firstTime, lastTime, 200) # For duration correlation
            newtimes = np.linspace(startTime, endTime, 500) # For full-time correlation
            tokVals = np.vstack((np.array([getPrice(tokens[i],t) for t in newtimes]),np.array([getPrice(tokens[j],t) for t in newtimes])))
            xs = np.linspace(firstTime, lastTime, 100)
            c = np.corrcoef(tokVals)[0,1]

            #corrcoef[i,j] = c * times2
            #corrcoef[j,i] = c * times2

            #corrcoef[i,j] = c * np.log(times2)
            #corrcoef[j,i] = c * np.log(times2)

            corrcoef[i,j] = c
            corrcoef[j,i] = c

            #p1 = np.array([getPrice(tokens[i], x) for x in xs])
            #p2 = np.array([getPrice(tokens[j], x) for x in xs])
            #p1 = (1/np.std(p1)) * (p1 - np.mean(p1))
            #p2 = (1/np.std(p2)) * (p2 - np.mean(p2))
            #corrcoef[i,j] = np.linalg.norm(p2 - p1)
            #corrcoef[j,i] = np.linalg.norm(p2 - p1)

    return corrcoef

plt.figure()
# PLOT TOKEN PRICE TIME SERIES
plotTokenList = []
for testToken in testTokens:
    #if testToken[0] == '0':
    #    continue
    if not fixAnomolyPrices:
        try:
            pricelist = pricedict[testToken]
        except KeyError:
            print("Error with", testToken)
            continue

        xst = [z[0] for z in pricelist]
        yst = [z[1] for z in pricelist]

        while len(yst) >= 2 and yst[1] > yst[0]: # Wait until the price goes down
            xst = xst[1:]
            yst = yst[1:]

        if len(yst) == 0:
            continue

        """
        plt.figure()
        xs, ys = [], []
        width = 0.07
        window = 200
        for i in range(window,len(pricelist)-window):
            minind = i-window
            maxind = i+window
            lowlim = np.quantile(yst[minind:maxind], 0.5-width)
            uplim = np.quantile(yst[minind:maxind], 0.5+width)
            if lowlim < yst[i] and yst[i] < uplim:
                xs.append(xst[i])
                ys.append(yst[i])
        plt.plot(xs,ys)
        """

        #plt.figure()
        xs, ys = [], []
        width = 0.05
        window = (1/np.sqrt(len(xst))) * (np.max(xst) - np.min(xst))
        minind = 0
        maxind = 0
        for i in range(len(xst)):
            while xst[minind] < xst[i] - window:
                minind += 1
            while maxind != len(xst)-1 and xst[maxind] < xst[i] + window:
                maxind += 1
            """
            lowlim = np.quantile(yst[minind:maxind], 0.5-width)
            uplim = np.quantile(yst[minind:maxind], 0.5+width)
            if lowlim < yst[i] and yst[i] < uplim:
                xs.append(xst[i])
                ys.append(yst[i])
            """
            xs.append(xst[i])
            ys.append(np.median(yst[minind:maxind]))
    
        if len(ys) == 0:
            print("Issue with token", testToken)
            continue
    else:
        try:
            pricelist = pricedict[testToken]
        except KeyError:
            print("Error 1 with", testToken)
            continue

        xs = [z[0] for z in pricelist]
        ys = [z[1] for z in pricelist]

    xs = np.array(xs)
    ys = np.array(ys)
    ys -= np.mean(ys)
    if np.std(ys) == 0:
        print("STD error with", testToken)
        continue
    ys *= (1/np.std(ys))
    if any(ys < -10):
        print("Negative value for", testToken)
        continue
    #if any(xs < 5000000): # FIXME
    #    print("Too old for", testToken)
    #    continue

    # TEMPORARY FIXME
    ys = [y if y < 8 else 1 for y in ys]

    print(testToken)
    plotTokenList.append(testToken)
    plt.plot(xs,ys, linewidth=0.5)
plt.legend(plotTokenList)

print("Plot Token List")
print(plotTokenList)
#plt.figure()
c = corr2(plotTokenList)
print(c)
c = c > threshold
print(c.shape)
print(np.unique(c))
sns.clustermap(c, xticklabels=plotTokenList, yticklabels=plotTokenList)
#sns.clustermap(corr(plotTokenList), xticklabels=plotTokenList, yticklabels=plotTokenList)

plt.show()
print("Plot done")

# PAIRWISE CORRELATION OF ALL TOKENS
indices = []
for token in pricedict.keys():
    if token not in valence.keys():
        continue
    if valence[token] > 750:
        indices.append(token)

#fullcorr = corr(indices).filled(0.0)
fullcorr = corr2(indices)
index2num = {index: i for i, index in enumerate(indices)}
num2index = {i: index for i, index in enumerate(indices)}

np.save('corr', fullcorr)
np.save('index', np.array(indices))

print("Writing graph")
with open("tokenGraph/corrNodesPrice.csv", "w") as writefile:
    writer = csv.writer(writefile)
    writer.writerow(["Id","Label","Num","StartTime","EndTime","Valence","Currency"])
    for token in indices:
        writer.writerow([token,token,index2num[token],starttime[token],endtime[token],valence[token],str(token[0] != '0')])

with open("tokenGraph/corrEdgesPrice.csv", 'w') as writefile:
    writer = csv.writer(writefile)
    writer.writerow(["Source", "Target", "Weight"])
    for i in range(len(indices)):
        for j in range(i+1,len(indices)):
            if fullcorr[i,j] > threshold:
                #print(indices[i], indices[j])
                writer.writerow([indices[i], indices[j], fullcorr[i,j]])

while True:
    inputs = input("What tokens? ")
    try:
        testTokens = [num2index[int(i)] for i in inputs.split(',')]
    except ValueError:
        print("Bad input. Needs to be the index")
        continue

    plotTokenList = []
    for testToken in testTokens:
        try:
            pricelist = pricedict[testToken]
        except KeyError:
            print("Error with", testToken)
            continue

        xst = [z[0] for z in pricelist]
        yst = [z[1] for z in pricelist]

        while len(yst) >= 2 and yst[1] > yst[0]: # Wait until the price goes down
            xst = xst[1:]
            yst = yst[1:]

        if len(yst) == 0:
            continue

        #plt.figure()
        xs, ys = [], []
        width = 0.05
        window = (1/np.sqrt(len(xst))) * (np.max(xst) - np.min(xst))
        minind = 0
        maxind = 0
        for i in range(len(xst)):
            while xst[minind] < xst[i] - window:
                minind += 1
            while maxind != len(xst)-1 and xst[maxind] < xst[i] + window:
                maxind += 1
            xs.append(xst[i])
            ys.append(np.median(yst[minind:maxind]))
        if len(ys) == 0:
            print("Issue with token", testToken)
            continue

        xs = np.array(xs)
        ys = np.array(ys)
        ys -= np.mean(ys)
        if np.std(ys) == 0:
            continue
        ys *= (1/np.std(ys))
        if any(ys < -10):
            continue
        if any(xs < 5000000): # FIXME
            continue

        # TEMPORARY FIXME
        ys = [y if y < 8 else 1 for y in ys]

        plotTokenList.append(testToken)
        plt.plot(xs,ys, linewidth=1)
    plt.legend(plotTokenList)

    print(plotTokenList)
    #plt.figure()
    #sns.heatmap(corr(plotTokenList), xticklabels=plotTokenList, yticklabels=plotTokenList)

    plt.show()
