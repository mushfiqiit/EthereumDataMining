import csv
import sys
csv.field_size_limit(sys.maxsize)

addresses = set([])
with open("../../ethereum_data/specialAccounts.csv") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        addresses.add(row[0].lower())

indices = {}
with open("../../ethereum_data/filterEtherTransactions.csv", 'w') as writefile:
    writefile.write("hash,from_address,to_address,block_number,timestamp,value\n")
    for index in range(1,72):
        print(index)
        with open("../../ethereum_data/transaction_csvs/transactions%02d.csv" % index) as readfile:
            reader = csv.reader(readfile)
            for row in reader:
                if row[0][0] == 'h':
                    indices = {}
                    for i in range(len(row)):
                        indices[row[i]] = i
                    continue
                if row[0][0] == '0':
                    ha = row[indices["hash"]]
                    fa = row[indices["from_address"]]
                    ta = row[indices["to_address"]]
                    bt = row[indices["block_timestamp"]]
                    bn = row[indices["block_timestamp"]]
                    va = row[indices["value"]]
                    if fa in addresses or ta in addresses:
                        writefile.write("%s,%s,%s,%s,%s,%s\n" % (ha, fa, ta, bn, bt, va))
