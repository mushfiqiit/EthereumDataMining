import csv

addresses = set([])
with open("../../ethereum_data/specialAddresses.csv") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        addresses.add(row[0].lower())

indices = {}
with open("../../ethereum_data/token_graph/filterTokenGraphBidirTime250.csv", 'w') as writefile:
    writefile.write("Source, Target, Time, Weight\n")
    for index in range(20):
        print(index)
        with open("../../ethereum_data/token_graph/bidir/tokenGraph250Time%02d.csv" % index) as readfile:
            reader = csv.reader(readfile)
            for row in reader:
                if row[0][0] == 'f':
                    indices = {}
                    for i in range(len(row)):
                        indices[row[i]] = i
                        #print(row[i], '.')
                    continue
                if row[0][0] == '0':
                    fa = row[indices["from_address"]]
                    ta = row[indices["to_address"]]
                    bn = row[indices["Time"]]
                    va = row[indices["Weight"]]
                    if fa in addresses or ta in addresses:
                        writefile.write("%s,%s,%s,%s\n" % (fa, ta, bn, va))
