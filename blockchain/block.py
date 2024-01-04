from time import time
import hashlib
import json


class Block:
    def __init__(self, index: int, transactions: list, proof: int, previous_block_hash: str):
        self.index = index
        self.transactions = transactions
        self.proof = proof
        self.previous_block_hash = previous_block_hash
        self.timestamps = time()

    def hash(self):
        block_string = json.dumps(self.as_dict(), sort_keys=True).encode()

        return hashlib.sha256(block_string).hexdigest()

    def as_dict(self):
        block_dict = self.__dict__
        block_dict['transactions'] = list(map(lambda transaction: transaction.as_dict(), block_dict['transactions']))

        return block_dict
