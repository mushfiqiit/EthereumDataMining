# findForkJoinGraph.py
# Restricts the full transaction network to only the transactions that 
# are fork join, or at least seems like it (since it only looks at some
# of the network at a time, split up by time)

import csv
import numpy as np

fjNodes = set([])
with open("../../ethereum_data/forkJoin_nodes/forkJoinAddressAll.csv") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        fjNodes.add(row[0])

for fji in range(20):
    print(fji)

    with open('../../ethereum_data/token_csvs/token_transfers%02d.csv' % fji) as csvfile2:
        with open('../../ethereum_data/token_graph/forkJoin_graph/forkJoinGraph%02d.csv' % fji, 'w') as writefile:
            with open('../../ethereum_data/token_graph/forkJoin_graph/forkJoinGraphRes%02d.csv' % fji, 'w') as writefile2:
                with open('../../ethereum_data/token_graph/forkJoin_graph/forkJoinGraphTokens%02d.csv' % fji, 'w') as writefile3:
                    writefile.write("token_address,from_address,to_address,value,transaction_hash,log_index,block_number\n")
                    writefile2.write("from_address,to_address,block_number\n")
                    writefile3.write("from_token,to_token,block_number\n")
                    reader2 = csv.reader(csvfile2)
    
                    lastToken = {}
                    lastAddress = {}
                    for row in reader2:
                        if row[0][0] != '0':
                            indicies = {}
                            for i in range(len(row)):
                                indicies[row[i]] = i
                        else:
                            token = row[indicies["token_address"]]
                            ta = row[indicies["to_address"]]
                            fa = row[indicies["from_address"]]
                            if ta in fjNodes or fa in fjNodes:
                                writefile.write("%s,%s,%s,%s,%s,%s,%s\n" % (row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
                            if ta in fjNodes:
                                lastAddress[ta] = fa
                            if fa in fjNodes and fa in lastToken.keys():
                                writefile2.write("%s,%s,%s\n" % (lastAddress[fa],ta,row[indicies["block_number"]]))
                            if ta in fjNodes:
                                lastToken[ta] = token
                            if fa in fjNodes and fa in lastToken.keys():
                                writefile3.write("%s,%s,%s\n" % (lastToken[fa],token,row[indicies["block_number"]]))
