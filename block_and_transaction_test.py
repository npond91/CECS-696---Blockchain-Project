from Blockchain_Project import blockchain

# setup test chain
test_chain = blockchain()

# genesis block is already created by the class
# so we will add 2 test blocks
# with 'dummy' data
# and then print the blockchain output

# print contents of genesis block for reference
# from previous trials this is the expected output:
# index: 1
# timestamp:
# transactions: []
# proofOfWork: 100
# previousBlockHash = '1'
#
# this matches up with the supplied data for the genesis block in the constructor
print("Printing Entire Chain: ")
print(test_chain.chainBlockList)
print("\nFinalBlock in Chain: ")
print(test_chain.finaBlock)
print("\nproof_of_work attribute of finalBlock [index 1]: ", test_chain.finaBlock['proof_of_work'])

# add our first test block to the chain
# we will 'mine' the next block by calling the proofOfWork algorithm
# this will calculate find and return the proof of the next block
print("\nCreating First New Block: ")
previous_block = test_chain.finaBlock
print("proof_of_work attribute for previous_block [index 1] : ", previous_block['proof_of_work'])
new_proof = test_chain.proof_of_work(previous_block)
print("proof_of_work attribute for new block [index 2]: ", new_proof)

# creating an arbitrary 'reward' akin to mining a coin
# in this case it lets us know we successfully found the next proof
# we do this by adding a transaction to the list
test_chain.create_new_transaction(
    senderID="Node 0",
    receiverID="No Such Person has received a reward",
    value=10,
)
print("Create New Transaction(s) for Block [index 2]: ", test_chain.transactionList)

# now we have the data needed to create the new block
# so we do so, and append it to the blockchain
previous_hash = test_chain.hash(previous_block)
test_block1 = test_chain.create_new_block(new_proof, previous_hash)

# repeating the process to add a 2nd block
# this will illustrates the difference in the block hashes
print("\n\nCreating Second New Block: ")
previous_block = test_chain.finaBlock
print("proof_of_work attribute for previous_block [index 2]: ", previous_block['proof_of_work'])
new_proof = test_chain.proof_of_work(previous_block)
print("proof_of_work attribute for new block [index 3]: ", new_proof)

test_chain.create_new_transaction(
    senderID="Node 1",
    receiverID="Also No Such Person",
    value=10,
)
print("Create New Transaction(s) for Block [index 3]: ", test_chain.transactionList)

previous_hash = test_chain.hash(previous_block)
test_block2 = test_chain.create_new_block(new_proof, previous_hash)

# creating another dummy transaction
# this will not be 'visible' by calling the print statements below
# this transaction will be added to the transaction list to the next block
# the not yet created block [4]
test_chain.create_new_transaction(
    senderID="Alice",
    receiverID="Bob",
    value=2,
)
print("\nNOTE: This Transaction Will Not Be Stored In The Chain Until A New Block Is Created")
print("Create New Transaction(s) for Block [index 4]: ", test_chain.transactionList)

# now we print the blockchain again, to see the results
# printing the entire chain
#print(test_chain.chainBlockList)
# looking specifically at genesis block
print("\n\nResults of Block and Transaction Creation: ")
print("\nGenesis Block: ")
print(test_chain.chainBlockList[0])
# looking specifically at test_block1
print("\nTest Block 1: ")
print(test_chain.chainBlockList[1])
# looking specifically at test_block2
print("\nTest Block 2: ")
print(test_chain.chainBlockList[2])
# look at the 'finalBlock' Object
# verify it is the same
print("\nFinal Block (Same as Above?): ")
print(test_chain.finaBlock)


# print transaction list attribute of finalBlock to further the transaction list point
final_block = test_chain.finaBlock
print("\n\nTransaction List of finalBlock [index 3]: ", final_block['transactions'])

