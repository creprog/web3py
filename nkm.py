# need for ABI and keyfiles
import json
# Ethereum lib
from web3 import Web3

# creating object for interacting with blockchain (mainnet or ropsten)
w3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/"))

# Nakama contract ABI 
abi = json.loads('[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"_name","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"stop","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"spender","type":"address"},{"name":"tokens","type":"uint256"}],"name":"approve","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"from","type":"address"},{"name":"to","type":"address"},{"name":"tokens","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"_decimals","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"_totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"tokenOwner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"stopped","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"acceptOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"_symbol","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"to","type":"address"},{"name":"tokens","type":"uint256"}],"name":"transfer","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_symbol","type":"string"}],"name":"setSymbol","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"start","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_name","type":"string"}],"name":"setName","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"newOwner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"tokenOwner","type":"address"},{"name":"spender","type":"address"}],"name":"allowance","outputs":[{"name":"remaining","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"payable":true,"stateMutability":"payable","type":"fallback"},{"anonymous":false,"inputs":[{"indexed":true,"name":"_from","type":"address"},{"indexed":true,"name":"_to","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"tokens","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"tokenOwner","type":"address"},{"indexed":true,"name":"spender","type":"address"},{"indexed":false,"name":"tokens","type":"uint256"}],"name":"Approval","type":"event"}]')

# Nakama's contract address
contractAddress = "0x2ccf8d382c486327cD2a817f0c0AC911d65fbBf7"

# creating object linked to deployed Nakama's contract
nakama = w3.eth.contract(address = contractAddress, abi = abi)

#
#	Balance's functions
#

# 1 Ether = 1000000000000000000 Wei

# return Ether balance of address in 'Wei'
def getEthBalWei(_address):
	return w3.eth.getBalance(_address)

# return Ether balance of address in 'Ether'
def getEthBalance(_address):
	return w3.fromWei(w3.eth.getBalance(_address), 'ether')

# return Nakama balance of address in 'Wei'
def getNkmBalWei(_address):
	return nakama.functions.balanceOf(_address).call()

# return Nakama balance of address in 'Ether'
def getNkmBalance(_address):
	return w3.fromWei(nakama.functions.balanceOf(_address).call(), 'ether')

#
#	Creating new Ethereum address (wallet)
#

# seed for improving random
# returning new Ethereum LocalAccount Object
def newEthAcc(_seed):
	return w3.eth.account.create(_seed)

# returning new address and private key (Ethereum wallet)
def fastEthAcc(_seed):
	newAcc = w3.eth.account.create(_seed)
	return newAcc.address, w3.toHex(newAcc.privateKey)

# open wallet from file, returning private key
def openPrivateKey(_fileName, _filePassword):
    with open(_fileName) as f:
        encrypted_key = f.read()
    return w3.toHex(w3.eth.account.decrypt(encrypted_key, _filePassword))

# save to file Ethereum LocalAccount Object
def saveEthAcc(_savingAcc, _filePassword):
	encrypted = w3.eth.account.encrypt(_savingAcc.privateKey, _filePassword)
	with open(_savingAcc.address, 'w') as f:	f.write(json.dumps(encrypted))

# save to file Private Key (result will be same as Ethereum LocalAccount Object)
def savePrivateKey(_privateKey, _filePassword):
	encrypted = w3.eth.account.encrypt(_privateKey, _filePassword)
	with open(w3.eth.account.privateKeyToAccount(_privateKey).address, 'w') as f:	f.write(json.dumps(encrypted))

#
#	Switching Accounts
#

# current address is w3.eth.defaultAccount

# easiest implenetation in setting account 
# btw need to think about
def setAcc(_address):
	w3.eth.defaultAccount = _address

# clearing after all, but need to test, not sure fully
def clearAcc():
	w3.eth.defaultAccount = 0

# set BigAccount (DANGEROUS)
def setBigAcc(_privateKey):
	thisAcc = {
		'address': w3.eth.account.privateKeyToAccount(_privateKey),
		'pkey': _privateKey
	}
	setAcc(thisAcc.address)

# clear BigAccount (DANGEROUS)
def clearBigAcc():
	thisAcc = {
		'address': 0,
		'pkey': 0
	}
	clearAcc

#
#	Ethereum Sending Functions
#

# !!!!! gas, gasPrice, chainId must be tested in mainnet
# 1 Ether = 1000000000000000000 Wei
# 'chainId': 1 (for mainnet) / 'chainId': 3 (for ropsten)

# send Ethereum in Wei
def sendEthWei(_to, _value, _privateKey, _gas=2000000, _gasPrice=30):
	# set sender (_from) account
	setAcc(w3.eth.account.privateKeyToAccount(_privateKey).address)
	# preparing transaction to send Ethereum
	transaction = {
    	'to': _to,
    	'value': _value,
    	'gas': _gas,
    	'gasPrice': _gasPrice,
    	'nonce': w3.eth.getTransactionCount(w3.eth.defaultAccount),
    	'chainId': 1
	}
	
	# signing transaction
	signed_txn = w3.eth.account.signTransaction(transaction, _privateKey)
	
	# sending transaction to blockchain
	w3.eth.sendRawTransaction(signed_txn.rawTransaction)
	clearAcc

# Will be depricated (DANGEROUS)
# sending Ethereum from BigAccount
def fastSend(_to, _value, _gas=2000000, _gasPrice=30):
	# need to add check if BigAccount not set
	# preparing transaction to send Ethereum
	transaction = {
    	'to': _to,
    	'value': _value,
    	'gas': _gas,
    	'gasPrice': _gasPrice,
    	'nonce': w3.eth.getTransactionCount(thisAcc.address),
    	'chainId': 1
	}
	# signing transaction
	signed = w3.eth.account.signTransaction(transaction, thisAcc.pkey)
	# sending transaction to blockchain
	w3.eth.sendRawTransaction(signed.rawTransaction)
	
#
#	Nakama Sending Functions
#

# send Nakama tokens in Wei
def sendNkmWei(_to, _value, _privateKey, _gas=8000000, _gasPrice=30):
	# set sender (_from) account
	setAcc(w3.eth.account.privateKeyToAccount(_privateKey).address)
	
	# preparing transaction to send Nakama tokens
	transaction = {
    	'gas': _gas,
    	'gasPrice': _gasPrice,
    	'nonce': w3.eth.getTransactionCount(w3.eth.defaultAccount),
    	'chainId': 1
	}

	# building transaction
	nkm_txn = nakama.functions.transfer(_to, _value).buildTransaction(transaction)
	# signing transaction
	signed_txn = w3.eth.account.signTransaction(nkm_txn, _privateKey)
	# sending transaction to blockchain
	w3.eth.sendRawTransaction(signed_txn.rawTransaction)
