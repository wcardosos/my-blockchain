from blockchain.transaction import Transaction


def test_as_dict():
    sut = Transaction('sender', 'recipient', 1)

    assert sut.as_dict() == {'sender': 'sender', 'recipient': 'recipient', 'amount': 1}
