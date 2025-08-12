import csv
import sys

csv.field_size_limit(sys.maxsize)

for tokenindex in range(2,6):
    transaction_hashes = set([])
    print("Token index", tokenindex)
    minind = 5+3*(tokenindex-1)
    maxind = min(5+3*(tokenindex), 20)
    for tokenindex2 in range(minind, maxind):
        with open("../../ethereum_data/token_csvs/token_transfers%02d.csv" % tokenindex2) as tokenfile:
            reader = csv.reader(tokenfile)
            for row in reader:
                if row[0] == 'token_address':
                    indices = {}
                    for i in range(len(row)):
                        indices[row[i]] = i
                else:
                    transaction_hashes.add(int(row[indices["transaction_hash"]],0))

    with open("../../ethereum_data/token_transactions/token_transactions%02d.csv" % tokenindex, 'w') as writefile:
        writer = csv.writer(writefile)
        for transferindex in range(1,71):
            print("\tTransaction file", transferindex)
            with open("../../ethereum_data/transaction_csvs/transactions%02d.csv" % transferindex) as transferfile:
                reader = csv.reader(transferfile)
                for row in reader:
                    if row[0] == 'hash':
                        if transferindex == 1:
                            writer.writerow(row)
                        indices = {}
                        for i in range(len(row)):
                            indices[row[i]] = i
                    else:
                        if int(row[indices['hash']], 0) in transaction_hashes:
                            writer.writerow(row)
