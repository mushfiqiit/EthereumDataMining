import csv
import numpy as np
import numpy.random as random

filename = "../ethereum_data/userData3"
with open(filename + ".csv") as readfile:
    with open(filename + "Sample.csv", "w") as writefile:
        reader = csv.reader(readfile)
        skip = 0
        for row in reader:
            if skip == 0:
                writefile.write("%s,%s,%s,%s\n" % (row[0], row[1], row[2], row[3]))
                skip = int(100 * random.random()) + 1
            skip -= 1
