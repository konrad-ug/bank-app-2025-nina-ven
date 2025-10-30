from src.account import Account
class Account_company(Account):
    def __init__(self, company_name, nip, balance=0.0):
        self.company_name = company_name
        self.nip = nip
        if len(self.nip) != 10:
            self.nip = "Invalid"
        self.balance=0
