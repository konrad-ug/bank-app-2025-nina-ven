from src.account import Account
class Account_company(Account):
    express_outgoing_transfer_fee = 5.0
    def __init__(self, company_name:str, nip:str):
        self.history = []
        self.balance = 0.0
        self.company_name = company_name
        self.nip = nip
        if len(self.nip) != 10:
            self.nip = "Invalid"


    def submit_for_loan(self, amount:float):
        if self.balance >= 2*amount and self.find_transfer_to_ZUS():
            self.balance += amount
            return True
        else:
            return False
        
    def find_transfer_to_ZUS(self):
        for transfer in self.history:
            if transfer == -1775:
                return True
        return False

