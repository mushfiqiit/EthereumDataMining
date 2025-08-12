import csv
import matplotlib.pyplot as plt
import numpy as np

times = []
with open("../ethereum_data/hists.csv") as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in reader:
        if row[0] == 'time':
            times = []
            for x in list(row[1:]):
                times.append(int(x))
        else:
            name = row[0]
            print(name)
            values = []
            for x in list(row[1:]):
                values.append(int(x))
            plt.cla()
            plt.clf()
            plt.step(times, values)
            plt.savefig(f'../ethereum_data/histograms/{name}.png', format='png')
