from typing import Optional, List
from urllib.parse import urlparse
from blockchain.block import Block
from blockchain.transaction import Transaction
from blockchain.proof_of_work import ProofOfWork
import requests


class Blockchain(object):
    def __init__(self):
        self.chain: List[Block] = []
        self.nodes = set()
        self.current_transactions: List[Transaction] = []

        # Create the genesis block
        self.add_block(previous_hash='1', proof=100)

    def add_block(self, proof: int, previous_hash: Optional[str] = None) -> Block:
        block = Block(
            len(self.chain) + 1,
            self.current_transactions,
            proof,
            previous_hash or self.last_block.hash()
        )

        self.current_transactions = []

        self.chain.append(block)

        return block

    def add_transaction(self, sender: str, recipient: str, amount: int) -> int:
        transaction = Transaction(sender, recipient, amount)

        self.current_transactions.append(transaction)

        return self.last_block.index + 1

    def register_node(self, address: str) -> None:
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def valid_chain(self, chain: list) -> bool:
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            proof_of_work = ProofOfWork(last_block.proof)
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")
            # Check that the hash of the block is correct
            if block['previous_hash'] != last_block.hash():
                return False

            # Check that the Proof of Work is correct
            if not proof_of_work.is_valid(block.proof):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self) -> bool:
        neighbours = self.nodes
        new_chain = None

        # We're only looking for chains longer than ours
        max_length = len(self.chain)

        # Grab and verify the chains from all the nodes in our network
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # Check if the length is longer and the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True

        return False

    @staticmethod
    def check_proof_of_work(last_proof: int) -> int:
        proof_of_work = ProofOfWork(last_proof)

        return proof_of_work.proof()

    @property
    def last_block(self) -> Block:
        return self.chain[-1]
