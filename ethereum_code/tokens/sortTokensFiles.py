import csv

for index in range(5,8):
    for half in [0, 1, 2, 3]:
        print("Reading file", index)
        tfrs = []
        tfrcounts = {}
        hashes = set([])
        with open("../../ethereum_data/token_csvs/token_transfers%d.csv" % index) as readfile:
            reader = csv.reader(readfile)
            for row in reader:
                if row[0] == 'token_address':
                    indices = {}
                    for i in range(len(row)):
                        indices[row[i]] = i
                else:
                    hexval = int(row[indices['transaction_hash']], 0)
                    bn = int(row[indices['block_number']])
                    if (index * 2000000 + half * 500000 < bn and bn <= index * 2000000 + (half+1) * 500000):
                        if hexval not in hashes:
                            hashes.add(hexval)
                            tfrs.append((bn,hexval))
                            tfrcounts[hexval] = 0
                        tfrcounts[hexval] += 1
        print("Found %d unique hashes" % len(tfrs))
        print("Sorting file", index)
        tfrs.sort(key = lambda z : z[1])
        tfrs.sort(key = lambda z : z[0])
        tfrtimes = [z[1] for z in tfrs]
        timeindex = 0
        temps = {}
        print("Writing file", index)
        with open("../../ethereum_data/token_csvs/token_transfers%dSorted%d.csv" % (index, half), 'w') as writefile:
            with open("../../ethereum_data/token_csvs/token_transfers%d.csv" % index) as readfile:
                reader = csv.reader(readfile)
                writer = csv.writer(writefile)
                for row in reader:
                    if row[0] == 'token_address':
                        writer.writerow(row)
                        indices = {}
                        for i in range(len(row)):
                            indices[row[i]] = i
                    else:
                        bn = int(row[indices['block_number']])
                        if (index * 2000000 + half * 500000 < bn and bn <= index * 2000000 + (half+1) * 500000):
                            hexval = int(row[indices['transaction_hash']], 0)
                            if hexval in temps.keys():
                                temps[hexval].append(row)
                            else:
                                temps[hexval] = [row]
                            while(timeindex < len(tfrtimes) and tfrtimes[timeindex] != hexval and tfrtimes[timeindex] in temps.keys() and tfrcounts[tfrtimes[timeindex]] == len(temps[tfrtimes[timeindex]])):
                                for txnrow in temps[tfrtimes[timeindex]]:
                                    writer.writerow(txnrow)
                                numbefore = len(temps.keys())
                                temps.pop(tfrtimes[timeindex])
                                numafter = len(temps.keys())
                                assert numafter == numbefore - 1
                                timeindex += 1
                            #if len(temps.keys()) > 100000:
                                #timeindex += 1
                                #print("Length Error")
                print("Working on final %d keys" % len(temps.keys()))
                while(timeindex < len(tfrtimes)):
                    #print("Needing work on remaining times")
                    if(tfrtimes[timeindex] in temps.keys()):
                        for txnrow in temps[tfrtimes[timeindex]]:
                            writer.writerow(txnrow)
                        temps.pop(tfrtimes[timeindex])
                    timeindex += 1
        print("Key length:", len(temps.keys()))
