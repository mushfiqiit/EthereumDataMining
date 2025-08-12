import csv
import numpy as np

for c in ['d','e','f']:
#for c in ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']:
    print("Start %c" % c)
    addresses = {}
    indices = {}
    for index in range(8):
        print(index)
        with open("../ethereum_data/token_csvs/token_transfers%d.csv" % index) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0][0] == 't':
                    for i in range(len(row)):
                        indices[row[i]] = i
                else:
                    ta = row[indices["to_address"]]
                    fa = row[indices["from_address"]]
                    bn = row[indices["block_number"]]
                    to = row[indices["token_address"]]
                    if not (c == to[2]):
                        continue
                    #try:
                        #addresses[ta].add(to)
                    #except KeyError:
                        #addresses[ta] = set([])
                        #addresses[ta].add(to)
                    #try:
                        #addresses[fa].add(to)
                    #except KeyError:
                        #addresses[fa] = set([])
                        #addresses[fa].add(to)
                    try:
                        addresses[to].add(ta)
                        addresses[to].add(fa)
                    except KeyError:
                        addresses[to] = set([ta])
                        addresses[to] = set([fa])
    
    print("Done %c" % c)
    with open("../ethereum_data/tokensPerAddress%c.csv" % c, "w") as csvfile:
        csvfile.write("address,count\n")
        for address in addresses.keys():
            csvfile.write("%s," % address)
            for add in addresses[address]:
                csvfile.write("%s;" % add)
            csvfile.write("\n")
