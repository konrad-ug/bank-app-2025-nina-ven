class Account:
    def __init__(self):
        self.balance=0.0

    def transfer_in(self, amount: float) -> None:
        if amount > 0:
            self.balance += amount

    def transfer_out(self, amount: float) -> None:
        if amount > 0 and self.balance:
            self.balance -= amount




