import sys
import csv

csv.field_size_limit(sys.maxsize)

# Import and process the transactions
csvFile2 = None
csvWriter = None
jump = 200000
curr = 25
with open('../transactionsToBreak3.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    indicies = {}
    fromAddress = {}
    toAddress = {}
    for row in reader:
        if(row[0] == "hash"):
            # Make the array of indicies
            header = row
            for i in range(len(row)):
                indicies[row[i]] = i
        else:
            # Read data
            bn = int(row[indicies["block_number"]])
            if (bn % 10000 == 0):
                print("Currently processing block %d bn" % bn)
            if int(row[indicies["block_number"]]) >= curr * jump:
                    curr += 1
                    if(csvFile2 != None):
                        csvFile2.close()
                    csvFile2 = open('../ethereum_data/transaction_csvs/transactions%d~~.csv' % curr, 'w')
                    csvWriter = csv.writer(csvFile2, delimiter=',', quotechar='|')
                    csvWriter.writerow(header)
            csvWriter.writerow(row)
if(csvFile2 != None):
    csvFile2.close()

