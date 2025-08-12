import csv

for c in ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']:
    print("Processing partition %c" % c)
    usersPerToken = {}
    indices = {}
    for index in range(8):
        with open("../ethereum_data/token_csvs/token_transfers%d.csv" % index) as readfile:
            print("\tBlock %d" % index)
            reader = csv.reader(readfile)
            for row in reader:
                if row[0][0] == 't':
                    indices = {}
                    for i in range(len(row)):
                        indices[row[i]] = i
                elif row[0][0] == '0' and row[0][2] == c.lower():
                    to = row[indices["token_address"]]
                    ta = row[indices["to_address"]]
                    fa = row[indices["from_address"]]
                    bn = row[indices["block_number"]]
                    try:
                        usersPerToken[to].add(ta)
                        usersPerToken[to].add(fa)
                    except KeyError:
                        usersPerToken[to] = set([ta,fa])
    with open("../ethereum_data/usersPerToken/usersPerToken%c.csv" % c, 'w') as writefile:
        writefile.write("token,users\n")
        for token in usersPerToken.keys():
            writefile.write("%s,%d\n" % (token, len(usersPerToken[token])))
