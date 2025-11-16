class Account:
    express_outgoing_transfer_fee = 0.0
    def __init__(self):
        self.history=[]
        self.balance=0.0


    def transfer_in(self, amount: float) -> None:
        if amount > 0:
            self.balance += amount
            self.history.append(amount)

    def transfer_out(self, amount: float) -> None:
        if 0 < amount <= self.balance:
            self.balance -= amount
            self.history.append(-amount)

    def express_transfer_out(self, amount: float) -> None:
        if 0 < amount <= self.balance:
            self.balance -= amount + self.express_outgoing_transfer_fee
            self.history.append(-amount)
            self.history.append(-self.express_outgoing_transfer_fee)





