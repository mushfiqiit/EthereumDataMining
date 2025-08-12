import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import csv
import networkx as nx
from scipy.io import savemat

# ethereumetl export_blocks_and_transactions --start-block 10000000 --end-block 12000000 --blocks-output blocks.csv --transactions-output transactions.csv --provider-uri file://../../media/dheeman/Seagate\ Backup\ Plus\ Drive/ethereum_data/geth/geth.ipc & > output.txt

class Transfer():
	time = 0
	toAddress = ""
	fromAddress = ""
	amount = 0

	def __init__(self, time, toAddress, fromAddress, amount):
		self.time = time
		self.toAddress = toAddress
		self.fromAddress = fromAddress
		self.amount = amount

	def toString(self):
		return "%s,%s,%s,%s" % (self.time, self.toAddress, self.fromAddress, self.amount)

class Transaction():
	hash = 0
	time = 0
	toAddress = ""
	fromAddress = ""
	amount = 0

	def __init__(self, hash, time, toAddress, fromAddress, amount):
		self.hash = hash
		self.time = time
		self.toAddress = toAddress
		self.fromAddress = fromAddress
		self.amount = amount

	def toString(self):
		return "%s,%s,%s,%s,%s" % (self.hash, self.time, self.toAddress, self.fromAddress, self.amount)

class LiteTransfer():
	time = 0
	amount = 0

	def __init__(self, time, amount):
		self.time = time
		self.amount = amount

class AccountData():
	account = ""
	transfers = {}

	def __init__(self, account, transfers):
		self.account = account
		self.transfers = transfers

class TransactionData():
	def __init__(self):
		self.transactionsPerAddress = {}
		self.accounts = []

	def loadTransactionsData(self, startBlock, endBlock, accounts):
		self.accounts = accounts
		row1 = ["hash","nonce","block_hash","block_number","transaction_index", \
				"from_address","to_address","value","gas","gas_price","input", \
				"block_timestamp","max_fee_per_gas","max_priority_fee_per_gas", \
				"transaction_type"]
		indicies = {}
		for i in range(len(row1)):
			indicies[row1[i]] = i

		setAccounts = set(accounts)
		for blockNumber in range(startBlock, endBlock+1):
			with open("../ethereum_data/blockchain_csvs/transactions%d.csv" % blockNumber, 'r') as csvfile:
				reader = csv.reader(csvfile, delimiter=",", quotechar="|")
				for row in reader:
					if(len(row1) == len(row) and row[0][0] == '0'):
						fa = row[indicies["from_address"]]
						ta = row[indicies["to_address"]]
						va = int(row[indicies["value"]])
						ha = row[indicies["hash"]]
						time = int(row[indicies["block_timestamp"]])
						t = Transaction(ha, time, ta, fa, va)
						if(ta in setAccounts):
							if(ta in self.transactionsPerAddress.keys()):
								self.transactionsPerAddress[ta].append(t)
							else:
								self.transactionsPerAddress[ta] = [t]
						if(fa in setAccounts):
							if(fa in self.transactionsPerAddress.keys()):
								self.transactionsPerAddress[fa].append(t)
							else:
								self.transactionsPerAddress[fa] = [t]

		for ac in self.transactionsPerAddress.keys():
			self.transactionsPerAddress[ac].sort(lambda y: y.time)

	def loadAllTransactionsData(self, startBlock, endBlock):
		row1 = ["hash","nonce","block_hash","block_number","transaction_index", \
				"from_address","to_address","value","gas","gas_price","input", \
				"block_timestamp","max_fee_per_gas","max_priority_fee_per_gas", \
				"transaction_type"]
		indicies = {}
		for i in range(len(row1)):
			indicies[row1[i]] = i

		for blockNumber in range(startBlock, endBlock+1):
			with open("../ethereum_data/blockchain_csvs/transactions%d.csv" % blockNumber, 'r') as csvfile:
				reader = csv.reader(csvfile, delimiter=",", quotechar="|")
				for row in reader:
					if(len(row1) == len(row) and row[0][0] == '0'):
						fa = row[indicies["from_address"]]
						ta = row[indicies["to_address"]]
						va = int(row[indicies["value"]])
						ha = row[indicies["hash"]]
						time = int(row[indicies["block_timestamp"]])

						t = Transaction(ha, time, ta, fa, va)
						if(ta in self.transactionsPerAddress.keys()):
							self.transactionsPerAddress[ta].append(t)
						else:
							self.transactionsPerAddress[ta] = [t]
						if(fa in self.transactionsPerAddress.keys()):
							self.transactionsPerAddress[fa].append(t)
						else:
							self.transactionsPerAddress[fa] = [t]

		for ac in self.transactionsPerAddress.keys():
			self.transactionsPerAddress[ac].sort(lambda y: y.time)

		self.accounts = self.transactionsPerAddress.keys()

	def saveTransactionsData(self):
		row1 = ["hash", "time", "to_address", "from_address", "amount"]

		for ac in self.transactionsPerAddress.keys():
			with open("../ethereum_data/%s.csv" % ac, 'w') as csvfile:
				csvfile.write("hash,time,to_address,from_address,amount\n")
				for txn in self.transactionsPerAddress[ac]:
					csvfile.write("%s\n" % txn.toSring())

	def readTransactionsData(self, accounts):
		row1 = ["hash", "time", "to_address", "from_address", "amount"]
		indicies = {}
		for i in range(len(row1)):
			indicies[row1[i]] = i

		self.accounts = accounts
		for acc in accounts:
			self.transactionsPerAddress[acc] = []
			with open("../ethereum_data/%s.csv" % acc, 'r') as csvfile:
				reader = csv.reader(csvfile, delimiter=",", quotechar="|")
				for row in reader:
					id = row[indicies["hash"]]
					time = row[indicies["time"]]
					ha = row[indicies["to_address"]]
					fa = row[indicies["from_address"]]
					va = row[indicies["amount"]]
					t = Transaction(id, time, ha, fa, va)
					self.transactionsPerAddress[acc].append(t)

class TokenData():
	blockFilename = "blocks60to71.csv"

	def __init__(self):
		self.tokenName = ""

		self.blockTimes = {}
		self.blocksLoaded = False

		self.transfers = []
		self.transfersPerAddress = {}
		self.transfersLoaded = False

		self.bigTransactors = []
		self.bigTransactorsFound = False

		# Nested dict of total token transfered
		self.compTransfersPerAddress = {}
		# Nested dict of total transactions per address
		self.compTransferCountsPerAddress = {}
		self.compTransfersFound = False

		self.graphLabelMap = {}
		self.graphInverseLabel = {}
		self.labelsFound = False

		self.cancelRatios = {}
		self.cancellationsFound = False

	def loadBlocks(self):
		if(self.blockFilename == ""):
			raise Exception("Block filename needed")
		self.blockTimes = {}

		row1 = ["number","hash","parent_hash","nonce","sha3_uncles","logs_bloom", \
			"transactions_root","state_root","receipts_root","miner","difficulty", \
			"total_difficulty","size","extra_data","gas_limit","gas_used","timestamp", \
			"transaction_count","base_fee_per_gas"]
		indicies = {}
		for i in range(len(row1)):
			indicies[row1[i]] = i

		with open(self.blockFilename, 'r') as csvfile:
			reader = csv.reader(csvfile, delimiter=",", quotechar="|")
			for row in reader:
				if(len(row1) == len(row) and row[0].isnumeric()):
					self.blockTimes[int(row[indicies["number"]])] = int(row[indicies["timestamp"]])

		self.blocksLoaded = True

	def loadTransferData(self, tokenName, tokenAddress):
		tokenAddress = tokenAddress.lower()
		self.tokenName = tokenName

		if(not self.blocksLoaded):
			self.loadBlocks()

		row1 = ["token_address","from_address","to_address","value", \
			"transaction_hash","log_index","block_number"]
		indicies = {}
		for i in range(len(row1)):
			indicies[row1[i]] = i

		with open("%sData/%s_transfers.csv" % (tokenName, tokenName), 'r') as csvfile:
			reader = csv.reader(csvfile, delimiter=",", quotechar="|")
			for row in reader:
				if(len(row1) == len(row) and row[0][0] == '0'):
					if(tokenAddress == row[indicies["token_address"]]):
						bn = int(row[indicies["block_number"]])
						ta = row[indicies["to_address"]]
						fa = row[indicies["from_address"]]
						va = int(row[indicies["value"]])
						t = Transfer(time = self.blockTimes[bn], \
									 toAddress = ta, \
									 fromAddress = fa, \
									 amount = va)
						self.transfers.append(t)
						if(ta in self.transfersPerAddress.keys()):
							self.transfersPerAddress[ta].append( \
								LiteTransfer(self.blockTimes[bn], va))
						else:
							self.transfersPerAddress[ta] = \
								[LiteTransfer(self.blockTimes[bn], va)]
						if(fa in self.transfersPerAddress.keys()):
							self.transfersPerAddress[fa].append( \
								LiteTransfer(self.blockTimes[bn], -va))
						else:
							self.transfersPerAddress[fa] = \
								[LiteTransfer(self.blockTimes[bn], -va)]
		self.transfers.sort(key = lambda y: y.toAddress)
		self.transfers.sort(key = lambda y: y.time)

		for address in self.transfersPerAddress.keys():
			self.transfersPerAddress[address].sort(key = lambda y: y.time)

		self.transfersLoaded = True

	def loadTransferParsedGross(self, tokenName):
		self.tokenName = tokenName

		row1 = ["Address","Tokens Transfered","Timestamp"]
		indicies = {}
		for i in range(len(row1)):
			indicies[row1[i]] = i

		with open("%sData/grossInternalTransactions.csv" % tokenName, 'r') as csvfile:
			reader = csv.reader(csvfile, delimiter=",", quotechar="|")
			for row in reader:
				if(len(row1) == len(row) and row[0][0] == '0'):
					ad = row[indicies["Address"]]
					ti = int(row[indicies["Timestamp"]])
					va = int(row[indicies["Token Transfered"]])
					if(ta in self.transfersPerAddress.keys()):
						self.transfersPerAddress[ad].append(LiteTransfer(ti, va))
					else:
						self.transfersPerAddress[ad] = [LiteTransfer(ti, va)]

		for address in self.transfersPerAddress.keys():
			self.transfersPerAddress[address].sort(key = lambda y: y.time)

		self.transfersLoaded = True

	def loadTransferParsedNet(self, tokenName):
		self.tokenName = tokenName

		row1 = ["Address","Tokens Transfered","Timestamp"]
		indicies = {}
		for i in range(len(row1)):
			indicies[row1[i]] = i

		with open("%sData/netInternalTransactions.csv" % tokenName, 'r') as csvfile:
			reader = csv.reader(csvfile, delimiter=",", quotechar="|")
			for row in reader:
				if(len(row1) == len(row) and row[0][0] == '0'):
					ad = row[indicies["Address"]]
					ti = int(row[indicies["Timestamp"]])
					va = int(row[indicies["Token Transfered"]])
					if(ta in self.transfersPerAddress.keys()):
						self.transfersPerAddress[ad].append(LiteTransfer(ti, va))
					else:
						self.transfersPerAddress[ad] = [LiteTransfer(ti, va)]

		for address in self.transfersPerAddress.keys():
			self.transfersPerAddress[address].sort(key = lambda y: y.time)

		self.transfersLoaded = True

	def getAccountData(self, account):
		if(account in self.transfersPerAddress.keys()):
			return None
		else:
			return AccountData(account, self.transfersPerAddress[account])

	def printInfo(self):
		if(not self.transfersLoaded):
			raise Exception("Need to load data")

		print("Number of transfers: %d" % len(self.transfers))

		singleTransactors = 0
		maxTransactions = 0
		maxTransactionsAccount = ""
		for acc in self.transfersPerAddress.keys():
			if len(self.transfersPerAddress[acc]) == 1:
				singleTransactors += 1
			if len(self.transfersPerAddress[acc]) > maxTransactions:
				maxTransactions = len(self.transfersPerAddress[acc])
				maxTransactionsAccount = acc
		print("Number of single transactors: %d" % singleTransactors)
		print("Number of transactions from largest transactor: %d" % maxTransactions)
		print("Max transactor: %s" % maxTransactionsAccount)

		if(self.bigTransactorsFound):
			print("Number of big transactors: %d" % len(self.bigTransactors))

		if(self.cancellationsFound):
			largeCancelations = self.cancelRatios[self.cancelRatios > 0.40]
			print("Number of large cancellation accounts: %d" % len(largeCancelations))

	def printGraphLabels(self, labels):
		if(not self.transfersLoaded):
			raise Exception("Need to load data")

		if(not self.labelsFound):
			self.findGraphLabels()

		for label in labels:
			print("Label %4d <-> Account %s" % (label, self.graphInverseLabel[label]))

	def printTransactionAmountsForAddress(self, account):
		if(not self.transfersLoaded):
			raise Exception("Transfers weren't loaded")

		counts = {}
		for tfr in self.transfers:
			if tfr.toAddress == account:
				if tfr.fromAddress in counts.keys():
					counts[tfr.fromAddress] += tfr.amount
				else:
					counts[tfr.fromAddress] = tfr.amount

		for acc in counts.keys():
			print("%s : %.7f" % (acc, counts[acc] / 1.0e18))

	def printTransactionAmountsForLabel(self, label):
		if(not self.transfersLoaded):
			raise Exception("Transfers weren't loaded")

		if(not self.labelsFound):
			self.findGraphLabels()

		account = self.graphInverseLabel[label]
		counts = {}
		for tfr in self.transfers:
			if tfr.toAddress == account:
				if tfr.fromAddress in counts.keys():
					counts[tfr.fromAddress] += tfr.amount
				else:
					counts[tfr.fromAddress] = tfr.amount

		keys = []
		for acc in counts.keys():
			keys.append(self.graphLabelMap[acc])
		keys.sort(key=lambda y: counts[self.graphInverseLabel[y]])
		for k in keys:
			print("%s : %.7f" % (k, counts[self.graphInverseLabel[k]] / 1.0e18))

	def findCancellationRatios(self):
		for adr in self.transfersPerAddress.keys():
			count = 0
			for i in range(len(self.transfersPerAddress[adr])-1):
				if(self.transfersPerAddress[adr][i].amount + self.transfersPerAddress[adr][i+1].amount == 0):
					count += 1
			self.cancelRatios[adr] = 1.0*count / (len(self.transfersPerAddress[adr]))

		self.cancellationsFound = True

	def findGraphLabels(self):
		if(not self.transfersLoaded):
			raise Exception("Transfers weren't loaded")

		addresses = list(self.transfersPerAddress.keys())
		for i in range(1, len(addresses)+1):
			self.graphLabelMap[addresses[i-1]] = i
			self.graphInverseLabel[i] = addresses[i-1]

		self.labelsFound = True

	def findLargeTransactors(self, threshold):
		if(self.bigTransactorsFound):
			return

		for acc in self.transfersPerAddress.keys():
			if len(self.transfersPerAddress[acc]) >= threshold:
				self.bigTransactors.append(acc)

		self.bigTransactorsFound = True

	def findCompressedTotalTransactions(self):
		if(not self.transfersLoaded):
			raise Exception("Need to load data")

		self.compTransfersPerAddress = {}
		for tfr in self.transfers:
			if(not (tfr.toAddress in self.compTransfersPerAddress.keys())):
				self.compTransfersPerAddress[tfr.toAddress] = {}
				self.compTransferCountsPerAddress[tfr.toAddress] = {}
			if(tfr.fromAddress in self.compTransfersPerAddress[tfr.toAddress].keys()):
				self.compTransfersPerAddress[tfr.toAddress][tfr.fromAddress] += tfr.amount
				self.compTransferCountsPerAddress[tfr.toAddress][tfr.fromAddress] += 1
			else:
				self.compTransfersPerAddress[tfr.toAddress][tfr.fromAddress] = tfr.amount
				self.compTransferCountsPerAddress[tfr.toAddress][tfr.fromAddress] = 1

		self.compTransfersFound = True

	def plotInteractionsGraph(self, edgeThreshold, byCount = False, omittedNodes = [], cancelThreshold=-1.0):
		print("Omitted nodes: ", omittedNodes)

		if(not self.labelsFound):
			self.findGraphLabels()

		if(not self.compTransfersFound):
			self.findCompressedTotalTransactions()

		if(not self.cancellationsFound):
			self.findCancellationRatios()

		G = nx.Graph()
		count = 0
		if(byCount):
			for t1 in self.compTransferCountsPerAddress.keys():
				for t2 in self.compTransferCountsPerAddress[t1].keys():
					# Plot based on cancelations
					if(self.cancelRatios[t1] > cancelThreshold and self.cancelRatios[t2] > cancelThreshold):
						if(self.compTransferCountsPerAddress[t1][t2] >= edgeThreshold):
							if((self.graphLabelMap[t1] not in omittedNodes) and (self.graphLabelMap[t2] not in omittedNodes)):
								G.add_edge(self.graphLabelMap[t1], self.graphLabelMap[t2])
								count += 1
		else:
			edgeThreshold *= 1.0e18
			for t1 in self.compTransfersPerAddress.keys():
				for t2 in self.compTransfersPerAddress[t1].keys():
					# Plot based on cancelations
					if(self.cancelRatios[t1] > cancelThreshold and self.cancelRatios[t2] > cancelThreshold):
						if(self.compTransfersPerAddress[t1][t2] >= edgeThreshold):
							if((self.graphLabelMap[t1] not in omittedNodes) and (self.graphLabelMap[t2] not in omittedNodes)):
								G.add_edge(self.graphLabelMap[t1], self.graphLabelMap[t2])
								count += 1
		print("Edge count: %d" % count)

		nx.draw_networkx(G)

		ax = plt.gca()
		ax.margins(0.20)
		plt.axis("off")
		plt.show()

	def plotAccountTimeSeries(self, account):
		if(not self.transfersLoaded):
			raise Exception("Need to load data")

		times = []
		values = []
		for tfr in self.transfersPerAddress[account]:
			times.append(tfr.time)
			values.append(tfr.amount)

		plt.hist(x = times, bins = 1000, histtype='step', \
			weights = values, cumulative=True)
		plt.show()

	def plotLabelTimeSeries(self, label):
		if(not self.transfersLoaded):
			raise Exception("Need to load data")

		if(not self.labelsFound):
			self.findGraphLabels()

		account = self.graphInverseLabel[label]

		times = []
		values = []
		for tfr in self.transfersPerAddress[account]:
			times.append(tfr.time)
			values.append(tfr.amount)

		plt.hist(x = times, bins = 1000, histtype='step', \
			weights = values, cumulative=True)
		plt.show()

	def saveMatrix(self):
		if(not self.compTransfersFound):
			self.findCompressedTotalTransactions()

		fa=[]
		ta=[]
		va=[]
		for toAddress in self.compTransfersPerAddress.keys():
			for fromAddress in self.compTransfersPerAddress[toAddress].keys():
				fa.append(fromAddress)
				ta.append(toAddress)
				va.append(self.compTransfersPerAddress[toAddress][fromAddress])

		mdic = {"fromAddress":np.array(fa), "toAddress":np.array(ta), "value":np.array(va, dtype=str)}
		savemat("tornData/tornMatrix.mat", mdic)

	def saveGraphLabels(self):
		if(not self.transfersLoaded):
			raise Exception("Need to load data")

		if(not self.labelsFound):
			self.findGraphLabels()

		with open("graphLabels.csv", 'w') as csvfile:
			csvfile.write("Label, Account\n")
			for label in self.graphInverseLabel.keys():
				csvfile.write("%d, %s\n" % (label, self.graphInverseLabel[label]))
