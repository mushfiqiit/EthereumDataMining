import sys
import csv
import pandas as pd

csv.field_size_limit(sys.maxsize)

fidelity = 2628000 # number of seconds in a month

blockToTime = {}
for i in range(6):
    #with open("../../ethereum_data/block_csvs/blocks%d.csv" % i) as csvfile:
    with open("../../ethereum_data/block_csvs/blocks%d.csv" % i, encoding="utf8", errors='ignore') as csvfile:
        reader = pd.read_csv(csvfile, delimiter=",", quotechar="|")
        for index, row in reader.iterrows():
            if row[0][0] == 'n':
                print(row)
                indicies = {}
                for i in range(len(row)):
                    indicies[row[i]] = i
            else:
                try:
                    num = row[indicies["number"]]
                    ti = row[indicies["timestamp"]]
                    blockToTime[int(num)] = int(ti)
                except Exception:
                    pass

print("Blocks Loaded")
while True:
#with open("../ethereum_data/monthlyTransfers.csv", "w") as csvfile:
#    csvfile.write("fromAddress,toAddress,value,count,time\n")
    thistime = -1
    lasttime = -1
    currtime = 0
    valuesByAddress = {}
    timesByAddress = {}
    for i in range(8):
        with open("../../ethereum_data/token_csvs/token_transfers%d.csv" % i) as csvfile2:
        #with open("../../ethereum_data/transaction_csvs/transactions%02d.csv" % i) as csvfile2:
            reader = csv.reader(csvfile2, delimiter=",", quotechar="|")
            for row in reader:
                try:
                    #if row[0][0] == 'h': # hash
                    if row[0][0] == 't': # hash
                        indicies = {}
                        for i in range(len(row)):
                            indicies[row[i]] = i
                    else:
                        fa = row[indicies["from_address"]]
                        ta = row[indicies["to_address"]]
                        va = int(row[indicies["value"]])
                        #ti = int(row[indicies["block_timestamp"]])
                        ti = blockToTime[int(row[indicies["block_number"]])]
                        if thistime == -1:
                            lasttime = ti
                        thistime = ti
    
                        # Save every current value
                        if thistime - lasttime > fidelity:
                            with open("../../ethereum_data/month_data/monthlyTransfers%02d.csv" % currtime, "w") as csvfile:
                                print("Currtime: %2d  Thistime: %d" % (currtime, thistime))
                                csvfile.write("fromAddress,toAddress,value,count,time,timestamp\n")
                                lasttime += fidelity
                                for fromAddress in valuesByAddress.keys():
                                    for toAddress in valuesByAddress[fromAddress].keys():
                                        if valuesByAddress[fromAddress][toAddress] > 0:
                                            csvfile.write("%s,%s,%d,%d,%d,%d\n" % (fromAddress, toAddress, valuesByAddress[fromAddress][toAddress], timesByAddress[fromAddress][toAddress], currtime, thistime))
                                            valuesByAddress[fromAddress][toAddress] = 0
                                            timesByAddress[fromAddress][toAddress] = 0
                                currtime += 1
                            #lasttime = thistime
                            #for fromAddress in valuesByAddress.keys():
                            #    for toAddress in valuesByAddress[fromAddress].keys():
                            #        if valuesByAddress[fromAddress][toAddress] > 0:
                            #            csvfile.write("%s,%s,%d,%d,%d\n" % (fromAddress, toAddress, valuesByAddress[fromAddress][toAddress], timesByAddress[fromAddress][toAddress], currtime))
                            #            valuesByAddress[fromAddress][toAddress] = 0
            
                            #            timesByAddress[fromAddress][toAddress] = 0
                            #currtime += 1

                        # Add value
                        if fa not in valuesByAddress.keys():
                            valuesByAddress[fa] = {}
                            timesByAddress[fa] = {}
                        if ta not in valuesByAddress[fa].keys():
                            valuesByAddress[fa][ta] = 0
                            timesByAddress[fa][ta] = 0
                        valuesByAddress[fa][ta] += va
                        timesByAddress[fa][ta] += 1
                except UnicodeDecodeError:
                    continue
    break
