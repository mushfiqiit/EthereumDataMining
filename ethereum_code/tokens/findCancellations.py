# findCancellations.py
# Searches through sections of the transaction csvs and finds all transactions that
# are immediately cancelled (a->b then b->a with equal weights)

import csv
import sys
csv.field_size_limit(sys.maxsize)

row1 = ["hash","nonce","block_hash","block_number","transaction_index","from_address", \
        "to_address","value","gas","gas_price","input","block_timestamp", "max_fee_per_gas", \
        "max_priority_fee_per_gas","transaction_type"]

indicies = {}
for i in range(len(row1)):
    indicies[row1[i]] = i

cancellations = {}
counts = {}
lastAmount = {}

#for number in range(1,26):
for number in range(1,72):
    print(number)
    with open("../../ethereum_data/transaction_csvs/transactions%d.csv" % number) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            if(row[0][0] != '0'):
                continue
            ta = row[indicies["to_address"]]
            fa = row[indicies["from_address"]]
            va = int(row[indicies["value"]])
            ti = row[indicies["block_timestamp"]]

            if(ta not in cancellations.keys()):
                counts[ta] = 1
                cancellations[ta] = 0
            else:
                counts[ta] += 1
                if(abs(lastAmount[ta]+va) == 0) and va != 0:
                    cancellations[ta] += 1
            lastAmount[ta] = va
            if(fa not in cancellations.keys()):
                counts[fa] = 1
                cancellations[fa] = 0
            else:
                counts[fa] += 1
                if(abs(lastAmount[fa]+(-va)) == 0) and va != 0:
                    cancellations[fa] += 1
            lastAmount[fa] = -va

print("Saving data")
with open("../../ethereum_data/cancellations.csv", 'w') as csvfile:
    for acc in cancellations.keys():
        csvfile.write("%s,%.7f\n" % (acc, 1.0*cancellations[acc]/counts[acc]))
