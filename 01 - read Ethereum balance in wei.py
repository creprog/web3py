from web3 import Web3

w3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/"))

address = input("Input Ethereum address")
print(w3.eth.getBalance(address))