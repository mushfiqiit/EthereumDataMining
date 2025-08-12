## Transaction and Token analysis for Ethereum

#### compressTransactions
For every account in the network, this script finds the total
amount of ether transacted with this account as well as the
total number of transactions that this account was involed
with.

#### evm
DOES NOT WORK AS INTENDED
This script utilizes pre-built python libraries that allow for
direct access to the Ethereum Virtual Machine in order to use
evm-specific commands that aren't readily available from 
ethereumetl.

#### findCancellations
For each account in the network, this script looks through every
transaction done by this node and counts the number of times
the account has neighboring transactions that are 'equal and
opposite'

#### findHistograms
For each account in the network, this script takes finds the
accounts that have the highest token transfer rates and then 
plots their interaction time-series.

#### findMaxTransactions
From some preprocessed files, this script will print the 
accounts with the highest transaction rate in and out of the 
node.

#### findMaxUsers
This script separates every transaction into a count of
transactions for each individual address. It then finds the
largest transactions in the network and saves them to
files in ethereum\_data with `Max` in their name.

#### findTokenTransactions
For a specific token address, this script takes all of the
token transfers and finds their associated transaction in 
the ethereum network, which allows for seeing the amount 
of ether spent overtime on transactions related to this
token.

#### findTokenTransfers
For a specific token address, this script sifts through all
the token data found and saves all occurences of the
specific token to another file for analysis with `tokana`.

#### findTransfersAmountsPerAddress
For each account in the network, this script finds the 
number of times this account create a transaction in the
network. It then saves these values to a csv in 
`ethereum\_data`.

#### monthlyTransactions
This script goes through every transaction in the network,
condensing parallel transactions in the same month into one
single, larger transaction. Each month's data is saved to
a different file as a csv.

#### plotHistograms
This script takes the output of `findHistograms` and plots
the data, saving the images to `ethereum\_data`.

#### sliceCsvs
This script takes the large transaction files found with
`ethereumetl` and separates them into smaller files which
makes file transfer easier. 

#### splitTokensByAddress
This script takes all of the loaded token data and separates 
them into different files based on the relevant token.

#### testForIsContract
DOES NOT WORK  
Takes an account id and asks the running geth node 
if the account has smart contract code associated 
with it
