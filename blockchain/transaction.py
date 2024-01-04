class Transaction:
    def __init__(self, sender: str, recipient: str, amount: int):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount

    def as_dict(self):
        return self.__dict__
