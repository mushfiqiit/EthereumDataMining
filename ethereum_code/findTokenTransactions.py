# findTokenTransactions.py
# Of the Uniswap transactions, find their associated Ethereum transactions
# to see how expensive uniswap tokens are overtime in terms of Ether

import sys
import csv

csv.field_size_limit(sys.maxsize)

indices = {}
transactionIndicies = set([])
tokenTraded = {}

#token = '0x1f9840a85d5af5bf1d1762f925bdaddc4201f984'
total = 100

tokens = []
curr = 0
with open('../ethereum_data/token_freq.csv') as readfile:
    reader = csv.reader(readfile)
    for row in reader:
        if row[1][0] == '0':
            tokens.append(row[1])
            curr += 1
            if curr == total:
                break

for token in tokens:
    print("Token", token)
    with open('../ethereum_data/token_csvs_separated/%s.csv' % token) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            if(row[0] == "token_address"):
                for i in range(len(row)):
                    indices[row[i]] = i
            else:
                transactionIndicies.add(row[indices["transaction_hash"]].lower())
                tokenTraded[row[indices["transaction_hash"]]] = row[indices["value"]]
    
    with open('../ethereum_data/token_transactions_separated/%s.csv' % token, 'w') as csvfile:
        csvfile.write("timestamp,token_value,ether_value,block_number\n")
        for ind in range(6):
            print("Currently processing file %d" % ind)
            with open('../ethereum_data/token_transactions/token_transactions%02d.csv' % ind) as csvfile2:
                reader = csv.reader(csvfile2, delimiter=',', quotechar='|')
                for row in reader:
                    if(row[0] == 'hash'):
                        indices = {}
                        for i in range(len(row)):
                            indices[row[i]] = i
                    else:
                        hashVal = row[0].lower()
                        if(hashVal in transactionIndicies):
                            if(row[indices["value"]] != "0"):
                                csvfile.write("%s,%s,%s,%s\n" % (row[indices["block_timestamp"]], tokenTraded[hashVal], row[indices["value"]], row[indices['block_number']]))
