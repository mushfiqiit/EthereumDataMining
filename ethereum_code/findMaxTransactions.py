# findMaxTransactions.py
# Save only the transactions relating to the addresses that have the largest
# in-degrees and out-degrees

import csv

maxFromList = []
with open('../ethereum_data/transactionsMaxFromAddress.txt', 'r') as csvfile:
	maxFromList = csvfile.read().replace("[", "").replace("]", "").replace(",", "").replace("'", "").split(" ")
print(maxFromList)

with open('../ethereum_data/transactionsMaxToAddress.txt', 'r') as csvfile:
	maxToList = csvfile.read().replace("[", "").replace("]", "").replace(",", "").replace("'", "").split(" ")
print(maxToList)

with open('../transactions.csv', newline='') as csvfile:
	with open('../ethereum_data/maxFromTransactions.csv', 'w', newline='') as returnfromfile:
		with open('../ethereum_data/maxToTransactions.csv', 'w', newline='') as returntofile:
			reader = csv.reader(csvfile, delimiter=',', quotechar='|')
			fromWriter = csv.writer(returnfromfile, delimiter=',', quotechar='|')
			toWriter = csv.writer(returntofile, delimiter=',', quotechar='|')
			indicies = {}
			fromAddress = {}
			toAddress = {}
			for row in reader:
				if(row[0] == "hash"):
					fromWriter.writerow(row)
					toWriter.writerow(row)
					# Make the array of indicies
					for i in range(len(row)):
						indicies[row[i]] = i
				else:
					if row[indicies["from_address"]] in maxFromList:
						fromWriter.writerow(row)
					if row[indicies["to_address"]] in maxToList:
						toWriter.writerow(row)
