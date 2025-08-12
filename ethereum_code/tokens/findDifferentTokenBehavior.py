# findDifferentTokenBehavior.csv
# Finds certain properties about different tokens, 
# including if they only have transactions in the 
# first 1000 blocks of them being around, or if they
# have a larger number of transactions

import csv
import math

files = []
with open("../../ethereum_data/token_csvs_big_filenames.csv") as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in reader:
        files = list(row)
        break

stopAfterAFew = False

keyList = ["Name","Count","0%","5%","100%","5% Proportion","Within 1000 blocks"]
printList = ["Name","5% Proportion","0%","Within 1000 blocks","Count"]
data = {}
count = 0
for filename in files:
    print(filename)
    if len(filename) < 10:
        continue
    token = filename[:-4]
    count += 1
    if stopAfterAFew and count >= 100:
        break
    data[filename[:-4]] = {"Name":token}
    with open("../../ethereum_data/token_csvs_big/" + filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        transacts = []
        # token_address,from_address,to_address,value,transaction_hash,log_index,block_number
        firstTime = 0
        fstThousndBlcks = 0
        for row in reader:
            if row[0][0] == 't':
                indicies = {}
                for i in range(len(row)):
                    indicies[row[i]] = i
            else:
                va = row[indicies["value"]]
                bn = int(row[indicies["block_number"]])
                if firstTime == 0:
                    firstTime = bn
                elif bn < firstTime + 1000:
                    fstThousndBlcks += 1
                transacts.append((bn, va))
        transacts.sort(key = lambda y : y[0])
        data[token]["Count"] = len(transacts)
        data[filename[:-4]]["0%"] = (transacts[0])[0]
        data[filename[:-4]]["5%"] = (transacts[math.floor(0.05*len(transacts))])[0]
        data[filename[:-4]]["100%"] = (transacts[-1])[0]
        data[filename[:-4]]["5% Proportion"] = round((data[filename[:-4]]["5%"]-(transacts[3])[0])/((transacts[-1])[0]-(transacts[0])[0] + 1), 4)
        data[filename[:-4]]["Within 1000 blocks"] = round(1.0 * fstThousndBlcks / len(transacts), 8)

with open("../../ethereum_data/big_token_data.csv", 'w') as csvfile:
    for key in printList:
        csvfile.write(key)
        csvfile.write(",")
    csvfile.write("\n")
    for acc in data.keys():
        for key in printList:
            csvfile.write(str(data[acc][key]))
            csvfile.write(",")
        csvfile.write("\n")
