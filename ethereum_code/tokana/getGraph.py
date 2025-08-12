import tokana as ta

td = ta.TokenData()
td.loadTransferData('torn', '0x77777feddddffc19ff86db637967013e6c6a116c')
td.printInfo()
print()
td.printGraphLabels([8543, 8788, 8558])
print()
#td.plotInteractionsGraph(100000, omittedNodes=[51, 13681, 13682, 13677])
td.plotInteractionsGraph(500, byCount=True)
#td.plotLabelTimeSeries(7)
td.printTransactionAmountsForLabel(8543)
