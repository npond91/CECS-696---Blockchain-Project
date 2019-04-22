import hashlib

previous_block_hash = input("Enter Previous Block Hash: ")
previous_block_proof = input("Enter Previous Block Proof: ")
current_block_proof = input("Enter Current Block Proof: ")

# convert inputs into string
# string will be hashed
string_inputs = f'{previous_block_proof}{current_block_proof}{previous_block_hash}'.encode()

# calculate the SHA-256 Hash
# Note This is Identical to the Hashing Generated by the Blockchain
# see is_proof_valid() function
hash = hashlib.sha256(string_inputs).hexdigest()

# A 'valid' Hash for the Blockchain will begin with three leading zeroes, '000'
# Can confirm by visually inspecting the resulting hash
print("The Computed SHA-256 Hash Is: ", hash)