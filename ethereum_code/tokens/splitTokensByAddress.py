import csv

DATADIR = '../../ethereum_data/token_csvs/'
DESTDIR = '../../ethereum_data/token_csvs_separated/'

adrs = {}
saveThres = 0
count = 0
for i in range(20):
    print(i)
    with open(DATADIR + 'token_transfers%02d.csv' % i) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            count += 1
            if row[0][0] == 't':
                firstrow = row
                indicies = {}
                for j in range(len(row)):
                    indicies[row[j]] = j
            else:
                ad = row[indicies["token_address"]]
                ta = row[indicies["to_address"]]
                fa = row[indicies["from_address"]]
                
                try:
                    adrs[ad].append(row)
                except KeyError:
                    adrs[ad] = [row]
                #try:
                #    adrs[ta].append(row)
                #except KeyError:
                #    adrs[ta] = [row]
                #try:
                #    if fa != ta:
                #        adrs[fa].append(row)
                #except KeyError:
                #    adrs[fa] = [row]
            if count >= saveThres:
                for adr in adrs.keys():
                    if i == 0:
                        with open(DESTDIR + adr + '.csv', 'w', newline='') as fi:
                            writer = csv.writer(fi)
                            writer.writerow(firstrow)
                            for row in adrs[adr]:
                                writer.writerow(row)
                    else:
                        with open(DESTDIR + adr + '.csv', 'a', newline='') as fi:
                            writer = csv.writer(fi)
                            writer.writerow(firstrow)
                            for row in adrs[adr]:
                                writer.writerow(row)
                count = 0
                adrs = {}


for adr in adrs.keys():
    with open(DESTDIR + adr + '.csv', 'a', newline='') as fi:
        writer = csv.writer(fi)
        writer.writerow(firstrow)
        for row in adrs[adr]:
            writer.writerow(row)
