from src.account import Account
class Account_company(Account):
    express_outgoing_transfer_fee = 5.0
    def __init__(self, company_name:str, nip:str):
        self.company_name = company_name
        self.nip = nip
        if len(self.nip) != 10:
            self.nip = "Invalid"
        self.balance=0.0
        self.history=[]

