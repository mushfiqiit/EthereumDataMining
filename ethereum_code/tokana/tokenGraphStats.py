import csv
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import teneto as tg
import igraph as ig
import networkx as nx

labelfile = "Token_Labels.csv"
filename = "tokenGraph/bidir/tokenGraph250Time19Bidir.csv"

# Loading labels
labeldf = pd.read_csv(labelfile)
print(labeldf['Type'].unique())
labels = dict(zip(labeldf['Id'].values, labeldf['Type'].values))

# Stats calculations
df = pd.DataFrame()
if False: # Partial
    df = pd.read_csv(filename).dropna()
else:
    for fileindex in range(20):
        print(fileindex)
        filename = "tokenGraph/bidir/tokenGraph250Time%02dBidir.csv" % fileindex

        tempdf = pd.read_csv(filename, dtype={'Source': str, 'Target': str, 'Time': int, 'Weight': int, 'SourceAmount': float, 'TargetAmount': float}).dropna()
        df = df.append(tempdf)

df['SourceAmount'] = df['SourceAmount'].astype(float)
df['TargetAmount'] = df['TargetAmount'].astype(float)
df = df.loc[~(df['SourceAmount'].isin([0.0]))]
df = df.loc[~(df['TargetAmount'].isin([0.0]))]
df['RatioAmount'] = df['SourceAmount'].values / df['TargetAmount'].values
#df = df.loc[df['RatioAmount'] < 1e20]
df['Source Target'] = df['Source'] + ' ' + df['Target']
indices = {v : i for i, v in enumerate(list(set(df['Source'].values.tolist()).union(set(df['Target'].values.tolist()))))}
indicesinv = {indices[x] : x for x in indices.keys()}
df['SourceIndex'] = df['Source'].apply(lambda x: indices[x])
df['TargetIndex'] = df['Target'].apply(lambda x: indices[x])

smallCutoff = 3
smalltokens = df.groupby('Source').size()
smalltokens = smalltokens.index.to_numpy()[smalltokens.values <= smallCutoff]
virality = df.loc[~df['Source'].isin(smalltokens)]
virality = virality.loc[:,['Source','Time','Weight']].groupby('Source').apply(lambda x: max(x['Weight'].values[smallCutoff:] / x['Weight'].values[(smallCutoff-1):-1]))
virality = virality.sort_values()
virality = virality.apply(np.log10)
viral = virality.loc[virality.values >= 1].index.to_list()
print(virality)

addressdf = pd.DataFrame(index=df['Source'].unique())
edgesdf = pd.DataFrame(index=df['Source Target'].unique())

# Edge weights
if True:
    edgesdf['Weights'] = df.loc[:,['Source Target','Weight']].groupby(['Source Target']).sum()

# Triangular Closure Coefficients
if True: 
    temp = df.loc[:,["Source","SourceAmount"]].groupby(["Source"]).size()
    addressdf['Valence'] = temp.loc[addressdf.index.tolist()]
    addressdf = addressdf.sort_values("Valence")
    temp = df.loc[:,["Source","Target"]].groupby(["Source"])
    addressdf['Triangle'] = 0
    for ind in temp.indices:
        temp2 = temp.get_group(ind)['Target'].unique()
        if(len(temp2) == 1):
            continue
        temp3 = df.loc[df['Source'].isin(temp2) & df['Target'].isin(temp2)]['Source Target'].values
        addressdf.at[ind,'Triangle'] = len(set(temp3))

    addressdf['TriangleProb'] = addressdf['Triangle'] / addressdf['Valence']
    addressdf['TriangleDensity'] = addressdf['Triangle'] / addressdf['Valence'].pow(2)

    print(addressdf['TriangleDensity'].max())
    print(addressdf.index[addressdf['TriangleDensity'].argmax()])

addressdf['Viral'] = addressdf.index.isin(viral)
addressdf['Virality'] = virality

# Importance measures
g = nx.Graph()
g.add_edges_from(np.unique(df.loc[:,['SourceIndex','TargetIndex']].values, axis=0).tolist())

print(addressdf.columns)
print(addressdf.index)

if True:
    pr = nx.pagerank(g)
    addressdf['PageRank'] = [pr[indices[x]] for x in addressdf.index]

if True:
    print("Max Clique")
    maxcl = []
    for cl in nx.find_cliques(g):
        if len(maxcl) < len(cl):
            maxcl = cl
    print([indicesinv[x] for x in maxcl])

if False:
    print("Communities")
    from networkx.algorithms import community
    com = community.greedy_modularity_communities(g)
    print(com)
    print("Finished communities")

# Art only
tokens = labeldf.loc[labeldf['Type'] == 'Finance']['Id'].values
dfart = df.loc[df['Source'].isin(tokens) | df['Target'].isin(tokens)]

for token in tokens:
    dftoken = df.loc[df['Source'].isin([token]) | df['Target'].isin([token])]
    valence = len(set(dftoken['Source'].values).union(dftoken['Target'].values))
    valence = len(set(dftoken['Source'].values))

dflarge = df.loc[:,['Source Target','SourceAmount','TargetAmount']].groupby(['Source Target']).size() > 5
dflarge = df.loc[df['Source Target'].isin(dflarge.loc[dflarge.values].index.tolist())]
#res = df.groupby("Source Target")["SourceAmount"].quantile([0.30, 0.70]).unstack(level=1)
#dflarge = dflarge.loc[((res.loc[dflarge["Source Target"], 0.30] < dflarge["SourceAmount"].values) & (dflarge["SourceAmount"].values < res.loc[dflarge["Source Target"], 0.70])).values]

if True:
    print("Correlations")
    corr = dflarge.loc[:,['Source Target','SourceAmount','TargetAmount']].groupby(['Source Target']).corr(method='pearson')
    corr = pd.DataFrame(data={'corr':corr['SourceAmount'].values[1::2]}, index=corr.index[1::2])
    corr = corr.reset_index(level=[1]).drop(columns='level_1')
    corr = corr.fillna(0.0)
    edgesdf['corr'] = corr

    largecorr = (corr.loc[np.logical_and(0.9 < corr.values[:,0], corr.values[:,0] < 0.99)]).index
    dflarge = dflarge.loc[dflarge['Source Target'].isin(largecorr)]

# TRANSACTIONS FOR 2 TOKENS #
mode = df['Source Target'].mode()[0]
smode, tmode = mode.split(' ')

tempcorr = corr.loc[np.logical_and(0.9 < corr.values[:,0], corr.values[:,0] < 1.01)]
corrmode = tempcorr.index[np.argmax(tempcorr.values)]
scorrmode, tcorrmode = corrmode.split(' ')

adr1 = scorrmode
adr2 = tcorrmode
dftwo = df.loc[df['Source'].isin([adr1]) & df['Target'].isin([adr2])]

fig = plt.figure()
ax = fig.add_subplot()
ax.scatter(dftwo['SourceAmount'].values / dftwo['Weight'].values, dftwo['TargetAmount'].values / dftwo['Weight'].values, marker='.')
ax.set_xlabel("Source Amount")
ax.set_ylabel("Target Amount")

fig = plt.figure()
ax = fig.add_subplot()
#ax = fig.add_subplot(projection='3d')
#plt.hist(dftwo['RatioAmount'].values, bins=100)
ax.scatter(dftwo['RatioAmount'].values[:-1], dftwo['RatioAmount'].values[1:], marker='.')
ax.plot(dftwo['RatioAmount'].values[:-1], dftwo['RatioAmount'].values[1:], lw=0.5)
rmin = dftwo['RatioAmount'].min()
rmax = dftwo['RatioAmount'].max()
ax.plot([rmin, rmax], [rmin, rmax], lw=0.5, color='yellow')
ax.set_xlabel("Current")
ax.set_ylabel("Future")
#ax.scatter(dftwo['RatioAmount'].values[2:], dftwo['RatioAmount'].values[1:-1], dftwo['RatioAmount'].values[:-2], marker='.')

fig = plt.figure()
ax = fig.add_subplot()
ax.plot(dftwo['Time'].values, dftwo['RatioAmount'].values)

#plt.show()

# FINAL CALCULATIONS

print(addressdf)
print(edgesdf.head(20))

nodes2 = addressdf
nodes2['Type'] = [labels[t] if t in labels.keys() else "NA" for t in nodes2.index]
nodes2['Label'] = [x for x in nodes2.index]
nodes2['Id'] = [x for x in nodes2.index]
nodes2 = nodes2.loc[:,['Id','Label','Type','PageRank','TriangleDensity','Viral','Virality']]
nodes2.to_csv("corrNodes.csv",index=False)

edges2 = edgesdf.dropna().copy()
edges2['Source'] = [x.split(' ')[0] for x in edges2.index]
edges2['Target'] = [x.split(' ')[1] for x in edges2.index]
edges2['Weight'] = edges2.loc[:,'corr']
edges2 = edges2.loc[:,['Source','Target','Weight']]
edges2.to_csv("corrEdges.csv", index=False)