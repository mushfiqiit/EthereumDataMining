# findMaxUsers.py
# Find the accounts for a token that have the largest in-degrees
# and out-degrees

import sys
import csv

csv.field_size_limit(sys.maxsize)

number = 8

# Import and process the transactions
with open('../ethereum_data/transaction_csvs/transactions%d.csv' % number, newline='') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='|')
	indicies = {}
	fromAddress = {}
	toAddress = {}
	for row in reader:
		if(row[0] == "hash"):
			# Make the array of indicies
			for i in range(len(row)):
				indicies[row[i]] = i
		else:
			# Read data
			if row[indicies["from_address"]] in fromAddress:
				fromAddress[row[indicies["from_address"]]] += 1
			else:
				fromAddress[row[indicies["from_address"]]] = 1
			if row[indicies["to_address"]] in toAddress:
				toAddress[row[indicies["to_address"]]] += 1
			else:
				toAddress[row[indicies["to_address"]]] = 1

# Store the dictionary of fromAddress
with open('../ethereum_data/transactions/transactionsFromAddress%d.txt' % number, 'w') as csvfile:
	csvfile.write(str(fromAddress))
with open('../ethereum_data/transactions/transactionsToAddress%d.txt' % number, 'w') as csvfile:
	csvfile.write(str(toAddress))

sortedValues = list(fromAddress.values())
sortedValues.sort()
maxValues = sortedValues[-5:]
maxFromKeys = [key for key, value in fromAddress.items() if value in maxValues]
print("Max From Users")
print(maxFromKeys)

sortedValues = list(toAddress.values())
sortedValues.sort()
maxValues = sortedValues[-5:]
maxToKeys = [key for key, value in toAddress.items() if value in maxValues]
print("Max To Users")
print(maxToKeys)

with open('transactions/transactionsMaxFromAddress%d.txt' % number, 'w') as csvfile:
	csvfile.write(str(maxFromKeys))
with open('transactions/transactionsMaxToAddress%d.txt' % number, 'w') as csvfile:
	csvfile.write(str(maxToKeys))
