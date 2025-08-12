import csv

indices = {}
with open("../ethereum_data/block_csvs/blockTimes.csv", "w") as writefile:
    for i in range(3):
        with open("../ethereum_data/block_csvs/blocks%d.csv" % i) as readfile:
            reader = csv.reader(readfile)
            for row in reader:
                if row[0][0] == 'n':
                    indices = {}
                    for i in range(len(row)):
                        indices[row[i]] = i
                else:
                    writefile.write("%s,%s\n" % (row[indices["number"]], row[indices["timestamp"]]))
