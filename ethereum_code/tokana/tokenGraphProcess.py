import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import gaussian_kde

tokenAddress = '0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984'.lower()

dfta = pd.DataFrame()
dffa = pd.DataFrame()
for i in range(8):
    print("Working on index %d" % i)
    df = pd.read_csv("tokenGraph/tokenGraph7.csv")
    dfta = pd.concat([dfta, df.loc[df["to_address"] == tokenAddress]], ignore_index=True)
    dffa = pd.concat([dffa, df.loc[df["from_address"] == tokenAddress]], ignore_index=True)

#sns.kdeplot(x=dffa["Time"].to_numpy().astype(np.float))
print(len(dffa["Time"].to_numpy().astype(np.float)))
print(len(dffa["Weight"].to_numpy().astype(np.float)))
sns.kdeplot(data=dffa, x='Time', fill=True, bw_adjust=.2)
sns.kdeplot(data=dffa, x='Time', weights='Weight', fill=True, bw_adjust=.2)
#gaussian_kde(dffa["Time"].to_numpy().astype(np.float), weights=dffa["Weight"].to_numpy().astype(np.float))
print("Works???")
plt.show()