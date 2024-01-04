import hashlib


class ProofOfWork:
    def __init__(self, last_proof_value: int):
        self.last_proof_value = last_proof_value

    def proof(self):
        value = 0

        while self.is_valid(value) is False:
            value += 1

        return value

    def is_valid(self, value):
        guess = f'{self.last_proof_value}{value}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"
