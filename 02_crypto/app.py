from flask import Flask, jsonify, request
from mycoin import Blockchain
# Part 2 - Mining our Blockchain
from uuid import uuid4
# Creating a Web App
app = Flask(__name__)

#Creating address for the new Node
node_address = str(uuid4()).replace("-","")

# Creating a Blockchain
blockchain = Blockchain()

# Mining a new block
@app.route('/mine_block', methods = ['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    blockchain.add_transaction(sender=node_address, receiver='Oleg', amount=10)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message': 'Congratulations, you just mined a block!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash'],
                'transactions': block['transactions']}
    return jsonify(response), 200

# Getting the full Blockchain
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200

# Checking if the Blockchain is valid
@app.route('/is_valid', methods = ['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': 'All good. The Blockchain is valid.'}
    else:
        response = {'message': 'Houston, we have a problem. The Blockchain is not valid.'}
    return jsonify(response), 200

@app.route('/add_transaction', methods = ['POST'])
def add_transaction():
    json = request.get_json()
    transactions_keys = ["sender", "receiver", "amount"]
    if not all (key in json for key in transactions_keys):
        return "Some elements are missing", 400
    index = blockchain.add_transaction(json['sender'], json['receiver'], json['amount'])
    response = {"message": f"This transaction will be added to block {index}"}
    return jsonify(response), 201

# Connecting new node
@app.route('/connect_node', methods = ['POST'])
def connect_node():
    json = request.get_json()
    nodes = json.get('nodes')
    if nodes is None:
        return "No nodes", 400
    for node in nodes:
        blockchain.add_node(node)
    response = {"message": "All nodes are connected.",
                "total_nodes": list(blockchain.nodes)}
    return jsonify(response), 201

@app.route('/replace_chain', methods = ['GET'])
def replace_chain():
    is_chain_replaced = blockchain.replace_chain()
    if is_chain_replaced:
        response = {'message': 'Chain is replaced',
                    'new_chain': blockchain.chain}
    else:
        response = {'message': 'Chain was not replaced',
                    'actual_chain': blockchain.chain}
    return jsonify(response), 200

# Running the app

app.run(host = '0.0.0.0', port = 5000)