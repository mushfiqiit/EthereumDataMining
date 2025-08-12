import csv

addresses = set([])
with open("../../ethereum_data/specialAddresses.csv") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        addresses.add(row[0].lower())

indices = {}
with open("../../ethereum_data/filterTokenTransactions.csv", 'w') as writefile:
    writefile.write("token_address,from_address,to_address,block_number,value\n")
    for index in range(20):
        print(index)
        with open("../../ethereum_data/token_csvs/token_transfers%02d.csv" % index) as readfile:
            reader = csv.reader(readfile)
            for row in reader:
                if row[0][0] == 't':
                    indices = {}
                    for i in range(len(row)):
                        indices[row[i]] = i
                    continue
                if row[0][0] == '0':
                    to = row[indices['token_address']]
                    fa = row[indices["from_address"]]
                    ta = row[indices["to_address"]]
                    bn = row[indices["block_number"]]
                    va = row[indices["value"]]
                    if fa in addresses or ta in addresses:
                        writefile.write("%s,%s,%s,%s,%s\n" % (to, fa, ta, bn, va))
