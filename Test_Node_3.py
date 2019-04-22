# Nick Pond
# CECS 696 - Spring 2019
# Master's Project
# Blockchain API

from uuid import uuid4
from flask import Flask, jsonify, request
from Blockchain_Project import blockchain

# instantiate the node
my_chain_app = Flask(__name__)

# Generate a unique address for the node
node_unique_identifier = str(uuid4()).replace('-', '')

# instantiate the Blockchain object
chain = blockchain()


#
# This section contains the URL functions
# Each function will correspond to a function of the blockchain object
#

# 1st - Mine
# GET request
# API implementation of the test_function
@my_chain_app.route('/mine', methods=['GET'])
def mine():
    # Check to see if the mining the new block will add to the chain, or this next block has already been mined
    # Comment this out to conduct 51 Percent Attack Example
    #get_consensus()

    # we will 'mine' the next block by calling the proofOfWork algorithm
    # this will calculate find and return the proof of the next block
    previous_block = chain.finaBlock
    new_proof = chain.proof_of_work(previous_block)

    # creating an arbitrary 'reward' akin to mining a coin
    # in this case it lets us know we successfully found the next proof
    # we do this by adding a transaction to the list
    chain.create_new_transaction(
        senderID="0",
        receiverID=node_unique_identifier,
        value=1,
    )

    # now we have the data needed to create the new block
    # so we do so, and append it to the blockchain
    previous_hash = chain.hash(previous_block)
    new_block = chain.create_new_block(new_proof, previous_hash)

    # Lastly, we create a response to provide feedback to the user
    response = {
        'message': "A New Block Has Been Forged",
        'index': new_block['index'],
        'timestamp': new_block['timestamp'],
        'transactions': new_block['transactions'],
        'proofOfWork': new_block['proof_of_work'],
        'previousBlockHash': new_block['previous_block_hash'],
    }

    return jsonify(response), 200

# 2nd - Transactions
# POST request - Adds new transactions to the block
# API implementation from the test)function


@my_chain_app.route('/transactions/new', methods=['POST'])
def create_new_transaction():

    data = request.get_json()

    # make sure the requisite fields exist
    # [sender, receiver, value]
    requirements = ['senderID', 'receiverID', 'value']
    if not all(x in data for x in requirements):
        return 'There are missing transaction values', 400

    # If all is well
    # Create the transaction by calling the method from the Blockchain
    index = chain.create_new_transaction(data['senderID'], data['receiverID'], data['value'])

    # Print some output for the user so we know the creation of the transaction was successful
    response = {'message': f'This transaction will be added to Block {index}'}

    return jsonify(response), 201

# 3rd - Display Chain
# Simple GET to print the chain data for the user to see
# also used for debugging to verify functionality


@my_chain_app.route('/show_chain', methods=['GET'])
def show_chain():

    response = {
        'chain': chain.chainBlockList,
        'length': len(chain.chainBlockList),
    }

    return jsonify(response), 200

# 4th - Register New Node
# POST request
# API implementation for Blockchain create_new_node method


@my_chain_app.route('/nodes/create', methods=['POST'])
def create_node():
    data = request.get_json()

    node_list = data.get('nodes')
    if node_list is None:
        return "This is not a valid list of Nodes", 400

    for node in node_list:
        chain.create_new_node(node)

    response = {
        'message': 'A new node has been added',
        'total_nodes': list(chain.nodeList)
    }

    return jsonify(response), 201

# 5th - Consensus
# GET request
# API implementation of Blockchain achieve_consensus method


@my_chain_app.route('/nodes/consensus', methods=['GET'])
def get_consensus():
    # call the achieve_consensus method, which returns T/F
    was_replaced = chain.achieve_consensus()

    if was_replaced:
        response = {
            'message': 'Our chain was replaced',
            'chain': chain.chainBlockList
        }
    else:
        response = {
            'message': 'Our chain was not replaced',
            'chain': chain.chainBlockList
        }

    return jsonify(response), 201


# Main method
# launch instance of server on port 5000
if __name__ == '__main__':
    my_chain_app.run(host='0.0.0.0', port=5003)
