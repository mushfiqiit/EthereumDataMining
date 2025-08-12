# testIsContract.py
# This uses the Etherscan api to test if an account is a contract account
# Only allows for a certain number of calls a day

from etherscan import Etherscan
import json
import csv
eth = Etherscan("ZVP4W5CH1EP444P6JFQR21U5WRG9Z41TCF")

def isContract(address):
    return (len((eth.get_contract_source_code(address=address.lower()))[0]['SourceCode']) > 0)

def printIsContract(address):
    if len((eth.get_contract_source_code(address=address.lower()))[0]['SourceCode']) > 0:
        print("Contract")
    else:
        print("Not contract")

def getContract(address):
    return (eth.get_contract_source_code(address=address.lower()))[0]

def printContract(address):
    print((eth.get_contract_source_code(address=address.lower()))[0].keys())

def printABI(address):
    print(json.loads(eth.get_contract_abi(address=address.lower()))[0])

#print(getContract("0x77777FeDdddFfC19Ff86DB637967013e6C6A116C"))
#printContract("0xdd3063b152262e632ae71efdfa2657a902026fdf")
#printABI("0x77777FeDdddFfC19Ff86DB637967013e6C6A116C")

keys = ['SourceCode', 'ABI', 'ContractName', 'CompilerVersion', 'OptimizationUsed', 'Runs', 'ConstructorArguments', 'EVMVersion', 'Library', 'LicenseType', 'Proxy', 'Implementation', 'SwarmSource']
with open('../ethereum_data/big_csvs_data.csv', 'w') as writefile:
    writefile.write("Contract")
    for key in keys:
        writefile.write("|" + key)
    writefile.write("\n")
    with open('../../ethereum_data/token_csvs_big_filenames.csv') as readfile:
        reader = csv.reader(readfile, delimiter=',', quotechar='|')
        for row in reader:
            for adrItr in row:
                adr = adrItr.lower()[:-4]
                try:
                    cont = getContract(adr)
                except Exception:
                    print(adr + " Except")
                    continue
                if cont == None:
                    print(adr + " No Code")
                    continue
                print(adr)
                writefile.write(adr)
                for key in keys:
                    writefile.write("|" + str(cont[key]))
                writefile.write("\n")
