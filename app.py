from flask import Flask, render_template, request, redirect, url_for
from web3.auto import w3
from web3 import Web3, HTTPProvider
from .forms import SetForm
import json

ADDRESS = '0xde961a60602afc50dfdcc533dd164061bb1fd6e7'  # Address where the contract is deployed.

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'
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
    block_number = web3.eth.blockNumber
    if not web3.isConnected:
        info = "Not Connected to blockchain! Please try again."
    info = "Connected to blockchain!"
    return render_template('index.html', title='Home', block_number=block_number, info=info)


@app.route("/get")
def get():
    instructor = contract.functions.getInfo().call()
    name = instructor[0]
    age = instructor[1]
    estimated_gas = contract.functions.getInfo().estimateGas()
    instructor = {"name": name, "age": age, "estimated_gas": estimated_gas}
    return render_template("get.html", title="Get Details", instructor=instructor)


@app.route("/set", methods=["GET", "POST"])
def set():
    if request.method == "POST":
        instructor_name = request.values.get('instructor_name')
        instructor_age = int(request.values.get('instructor_age'))
        estimated_gas = contract.functions.setInfo(instructor_name, instructor_age).estimateGas()
        tx_hash = contract.functions.setInfo(instructor_name, instructor_age).transact({'from': w3.eth.accounts[0]})
        tx_receipt = web3.eth.getTransactionReceipt(tx_hash)
        return redirect(url_for('get'))
    else:
        form = SetForm()
        return render_template('set.html', title="Set Details", form=form)

