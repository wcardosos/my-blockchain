from typing import Optional, List
from blockchain.block import Block
from blockchain.transaction import Transaction
from blockchain.proof_of_work import ProofOfWork


class Blockchain(object):
    def __init__(self):
        self.chain: List[Block] = []
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

    @staticmethod
    def check_proof_of_work(last_proof: int) -> int:
        proof_of_work = ProofOfWork(last_proof)

        return proof_of_work.proof()

    @property
    def last_block(self) -> Block:
        return self.chain[-1]
