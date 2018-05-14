from flask import Flask, render_template, request, redirect, url_for
from web3.auto import w3
from web3 import Web3, HTTPProvider
from .forms import SetForm, BurnForm

ADDRESS = '0xde961a60602afc50dfdcc533dd164061bb1fd6e7'  # Address where the contract is deployed.

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'
web3 = Web3(HTTPProvider('http://localhost:8545'))
eipAddress = web3.toChecksumAddress(ADDRESS)

abi = ({'type': 'function', 'payable': False, 'constant': False, 'name': 'approve', 'inputs': [{'type': 'address', 'name': '_spender'}, {'type': 'uint256', 'name': '_value'}], 'outputs': [{'type': 'bool', 'name': 'success'}], 'stateMutability': 'nonpayable'}, {'type': 'function', 'payable': False, 'constant': False, 'name': 'approveAndCall', 'inputs': [{'type': 'address', 'name': '_spender'}, {'type': 'uint256', 'name': '_value'}, {'type': 'bytes', 'name': '_extraData'}], 'outputs': [{'type': 'bool', 'name': 'success'}], 'stateMutability': 'nonpayable'}, {'type': 'function', 'payable': False, 'constant': False, 'name': 'burn', 'inputs': [{'type': 'uint256', 'name': '_value'}], 'outputs': [{'type': 'bool', 'name': 'success'}], 'stateMutability': 'nonpayable'}, {'type': 'function', 'payable': False, 'constant': False, 'name': 'burnFrom', 'inputs': [{'type': 'address', 'name': '_from'}, {'type': 'uint256', 'name': '_value'}], 'outputs': [{'type': 'bool', 'name': 'success'}], 'stateMutability': 'nonpayable'}, {'type': 'function', 'payable': False, 'constant': False, 'name': 'transfer', 'inputs': [{'type': 'address', 'name': '_to'}, {'type': 'uint256', 'name': '_value'}], 'outputs': [], 'stateMutability': 'nonpayable'}, {'anonymous': False, 'type': 'event', 'name': 'Transfer', 'inputs': [{'indexed': True, 'type': 'address', 'name': 'from'}, {'indexed': True, 'type': 'address', 'name': 'to'}, {'indexed': False, 'type': 'uint256', 'name': 'value'}]}, {'anonymous': False, 'type': 'event', 'name': 'Burn', 'inputs': [{'indexed': True, 'type': 'address', 'name': 'from'}, {'indexed': False, 'type': 'uint256', 'name': 'value'}]}, {'type': 'function', 'payable': False, 'constant': False, 'name': 'transferFrom', 'inputs': [{'type': 'address', 'name': '_from'}, {'type': 'address', 'name': '_to'}, {'type': 'uint256', 'name': '_value'}], 'outputs': [{'type': 'bool', 'name': 'success'}], 'stateMutability': 'nonpayable'}, {'type': 'constructor', 'payable': False, 'inputs': [{'type': 'uint256', 'name': 'initialSupply'}, {'type': 'string', 'name': 'tokenName'}, {'type': 'string', 'name': 'tokenSymbol'}], 'stateMutability': 'nonpayable'}, {'type': 'function', 'payable': False, 'constant': True, 'name': 'allowance', 'inputs': [{'type': 'address', 'name': ''}, {'type': 'address', 'name': ''}], 'outputs': [{'type': 'uint256', 'name': ''}], 'stateMutability': 'view'}, {'type': 'function', 'payable': False, 'constant': True, 'name': 'balanceOf', 'inputs': [{'type': 'address', 'name': ''}], 'outputs': [{'type': 'uint256', 'name': ''}], 'stateMutability': 'view'}, {'type': 'function', 'payable': False, 'constant': True, 'name': 'decimals', 'inputs': [], 'outputs': [{'type': 'uint8', 'name': ''}], 'stateMutability': 'view'}, {'type': 'function', 'payable': False, 'constant': True, 'name': 'name', 'inputs': [], 'outputs': [{'type': 'string', 'name': ''}], 'stateMutability': 'view'}, {'type': 'function', 'payable': False, 'constant': True, 'name': 'symbol', 'inputs': [], 'outputs': [{'type': 'string', 'name': ''}], 'stateMutability': 'view'}, {'type': 'function', 'payable': False, 'constant': True, 'name': 'totalSupply', 'inputs': [], 'outputs': [{'type': 'uint256', 'name': ''}], 'stateMutability': 'view'})

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
    account = request.args.get('account', default=1, type=int)
    account = account - 1
    acc_addr = w3.eth.accounts[account]
    acc_bal = contract.functions.balanceOf(acc_addr).call()
    estimated_gas = contract.functions.balanceOf(acc_addr).estimateGas()
    tx_hash = contract.functions.balanceOf(acc_addr).transact({'from': w3.eth.accounts[0]})
    tx_receipt = web3.eth.getTransactionReceipt(tx_hash)
    account_number = "User #" + str(account+1)
    data = {
        "account": account_number,
        "balance": acc_bal,
        "gas": estimated_gas,
        "tx_receipt": tx_receipt,
    }
    return render_template("get.html", title="Get Details", data=data)


@app.route("/set", methods=["GET", "POST"])
def set():
    if request.method == "POST":
        to_account = int(request.values.get('to_account'))
        account = w3.eth.accounts[to_account - 1]
        amount = int(request.values.get('amount'))
        # estimated_gas = contract.functions.transfer(account, amount).estimateGas()
        tx_hash = contract.functions.transfer(account, amount,).transact(
            {
                'from': w3.eth.accounts[0]
            }
        )
        tx_receipt = web3.eth.getTransactionReceipt(tx_hash)
        return redirect(url_for('get'))
    else:
        form = SetForm()
        return render_template('set.html', title="Set Details", form=form)


@app.route("/redeem", methods=["GET", "POST"])
def burn():
    if request.method == "POST":
        from_account = int(request.values.get('from_account'))
        account = w3.eth.accounts[from_account - 1]
        amount = int(request.values.get('amount'))
        # estimated_gas = contract.functions.transfer(account, amount).estimateGas()
        tx_hash = contract.functions.burn(amount).transact({'from': account})
        tx_receipt = web3.eth.getTransactionReceipt(tx_hash)
        return redirect(url_for('get'))
    else:
        form = BurnForm()
        return render_template('burn.html', title="Set Details", form=form)

