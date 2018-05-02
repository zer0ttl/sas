from flask import Flask, render_template, url_for
from web3.auto import w3
from web3 import Web3, HTTPProvider
import json

ADDRESS = '0xde961a60602afc50dfdcc533dd164061bb1fd6e7'  # Address where the contract is deployed.

app = Flask(__name__)
web3 = Web3(HTTPProvider('http://localhost:8545'))
eipAddress = web3.toChecksumAddress(ADDRESS)
abi = {"constant": False, "inputs": [{"name": "_fName", "type": "string"}, {"name": "_age", "type": "uint256"}],
       "name": "setInfo", "outputs": [], "payable": False, "stateMutability": "nonpayable", "type": "function"}, {
          "constant": True, "inputs": [], "name": "getInfo",
          "outputs": [{"name": "", "type": "string"}, {"name": "", "type": "uint256"}], "payable": False,
          "stateMutability": "view", "type": "function"}

contract = web3.eth.contract(address=eipAddress, abi=abi)


@app.route("/")
def index():
    a = web3.eth.blockNumber
    if not web3.isConnected:
        output = "Not Connected to Blockchain! Please try again."
    output = "<h1>Block number : {}</h1><hr>".format(a)
    # <h3><a href=''>Get</a><br><a href='{{ url_for('get') }}'>Set</a></h3>
    return output


@app.route("/get")
def get():
    instructor = contract.functions.getInfo().call()
    name = instructor[0]
    age = instructor[1]
    estimatedGas = contract.functions.getInfo().estimateGas()
    output = "<h1>Instructor Name : {} <br>Instructor Age : {}</h1><hr><h3>Estimated Gas required : {}</h3>".format(
        name, age, estimatedGas)
    return output


@app.route("/set/<name>/<age>")
def set(name=None, age=None):
    instructorName = str(name)
    instructorAge = int(age)
    estimatedGas = contract.functions.setInfo(instructorName, instructorAge).estimateGas()
    tx_hash = contract.functions.setInfo(instructorName, instructorAge).transact({'from': w3.eth.accounts[0]})
    tx_receipt = web3.eth.getTransactionReceipt(tx_hash)
    output = "Transaction completed successfully. Estimated Gas required : {}".format(estimatedGas)
    return output


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name='Sam'):
    return render_template('hello.html', name=name)
