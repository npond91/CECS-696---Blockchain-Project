# Nick Pond
# CECS 696 - Spring 2019
# Master's Project
# Simple Functioning Blockchain

import json
import hashlib
import requests
from time import time
from urllib.parse import urlparse


class blockchain(object):
    # the constructor for the block chain
    def __init__(self):
        self.chainBlockList = []
        self.transactionList = []
        self.nodeList = set()

        # creating the genesis block
        # this is very important as the genesis block is unique
        # it does not contain the requisite 'previous hash' as they do not exist
        # also the proof_of_work solution set is arbitrary
        # thus the genesis block kickstarts the entire chain
        self.create_new_block(previous_block_hash='1', proof_of_work=100)

    def create_new_block(self, proof_of_work, previous_block_hash):
        # creates a new block and adds it to the chain list
        #
        # index param: position of the block in the chain
        # timestamp param: the time the block was created
        # transactions param: list of transactions accrued by the previous block
        # proof_of_work param: the solution for the proof of work for this block
        # previous_block_hash param: the hash of the previous block

        block = {
            'index': len(self.chainBlockList) + 1,
            'timestamp': time(),
            'transactions': self.transactionList,
            'proof_of_work': proof_of_work,
            'previous_block_hash': previous_block_hash or self.hash(self.chainBlockList[-1]),
        }

        self.transactionList = []
        self.chainBlockList.append(block)

        return block

    def create_new_transaction(self, senderID, receiverID, value):
        # creates new transaction and adds it to the transaction list
        # this creates transactions for the next block
        # the current block is immutable
        # adding data to the current block would alter the hash

        self.transactionList.append({
            'senderID': senderID,
            'receiverID': receiverID,
            'value': value,
        })

        return self.finaBlock['index'] + 1

    def create_new_node(self, node_address):
        # Adds a new node to the set of nodes
        # set is used to ensure that there is only
        # a single instance of each node, keeping them unique

        node_url = urlparse(node_address)

        if node_url.netloc:
            self.nodeList.add(node_url.netloc)
        elif node_url.path:
            self.nodeList.add(node_url.path)
        else:
            raise ValueError('URL is Invalid')

    def validate_chain(self, chain):
        # verify if a Blockchain is valid
        # checking the hashes of the blocks, making sure they match where appropriate
        # verifying the proof of work for each block using 'is_proof_valid' method

        previous_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            current_block = chain[current_index]
            print(f'{previous_block}')
            print(f'{current_block}')
            print("\n\n\n")

            # Check the hash of the current_block is correct
            # Done by checking the hash of the current_block to the 'previousHash' of the previous block
            previous_block_hash = self.hash(previous_block)
            if current_block['previous_block_hash'] != previous_block_hash:
                return False

            # Next step, verify the Proof of Work
            if not self.is_proof_valid(previous_block['proof_of_work'], current_block['proof_of_work'], previous_block_hash):
                return False

            previous_block = current_block
            current_index = current_index + 1

        return True

    def achieve_consensus(self):
        # this is the Consensus algorithm
        # this method will resolve conflicts between nodes
        # a node will replace its chain with the longest chain present on the network
        # if no longer node is discovered 'our chain' is kept, return False

        neighbor_nodes = self.nodeList
        new_chain = None

        # Checking if there are any chains on the network longer than 'our own'
        # First step is to get the length of our current chain
        our_chain_length = len(self.chainBlockList)

        # Second step, verify the validity of the chains of the other nodes
        for node in neighbor_nodes:
            response = requests.get(f'http://{node}/show_chain')

            if response.status_code == 200:
                neighbor_chain = response.json()['chain']
                neighbor_chain_length = response.json()['length']

                # compare length of neighbor chain to 'our own'
                if neighbor_chain_length > our_chain_length and self.validate_chain(neighbor_chain):
                    new_chain = neighbor_chain
                    our_chain_length = neighbor_chain_length

        # If a longer chain is found, replace 'our own' with the new_chain
        if new_chain:
            self.chainBlockList = new_chain
            return True

        return False

    @staticmethod
    def hash(block):
        # creates the hash for the current block
        # using SHA256

        # put object data in string form and order dictionary
        # then run the aggregate block data through SHA256 function to generate the hash
        string = json.dumps(block, sort_keys=True).encode()
        blockHash = hashlib.sha256(string).hexdigest()

        return blockHash

    @property
    def finaBlock(self):
        # finds the last block in the chain list
        return self.chainBlockList[-1]

    def proof_of_work(self, finalBlock):
        # works with is_proof_valid() function
        # to find a hash collision that has 3 leading zeroes
        # the value 'proof_new_block' will continuously incremented until a collision is found

        proof_previous_block = finalBlock['proof_of_work']
        hash_previous_block = self.hash(finalBlock)

        proof_new_block = 0

        while self.is_proof_valid(proof_previous_block, proof_new_block, hash_previous_block) is False:
            proof_new_block = proof_new_block + 1

        return proof_new_block

    @staticmethod
    def is_proof_valid(proof_previous_block, proof_new_block, hash_previous_block):
        # validates the proof for the block
        # takes the proof_new_block and computes the hash
        # returns the hash if it has 3 leading zeroes
        # this makes the loop in proof_of_work end
        # completing the proof of work for the block

        current_guess = f'{proof_previous_block}{proof_new_block}{hash_previous_block}'.encode()
        current_hash_guess = hashlib.sha256(current_guess).hexdigest()

        if current_hash_guess[:3] == "000":
            return True
        else:
            return False
