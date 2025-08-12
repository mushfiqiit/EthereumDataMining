# findTokenGraph2.py

import csv
import numpy as np

timeRes = True

with open("../../ethereum_data/multiTransactions.csv", "w") as writefile:
    singleTransaction = set()
    multiTransaction = set()

    writer = csv.writer(writefile)
    for fji in range(20):
        print(fji)
    
        with open('../../ethereum_data/token_csvs/token_transfers%02d.csv' % fji) as csvfile2:
                reader2 = csv.reader(csvfile2)
    
                for row in reader2:
                    if row[0][0] != '0':
                        indicies = {}
                        for i in range(len(row)):
                            indicies[row[i]] = i
                    else:
                        #sth = row[indicies["transaction_hash"]]
                        #if not ('0' <= sth[2] and sth[2] <= '7'):
                            #continue
                        th = int(row[indicies["transaction_hash"]], 0)
                        if th in multiTransaction:
                            continue
                        if th in singleTransaction:
                            multiTransaction.add(th)
                            writer.writerow([th])
                            singleTransaction.remove(th)
                        else:
                            singleTransaction.add(th)
    
