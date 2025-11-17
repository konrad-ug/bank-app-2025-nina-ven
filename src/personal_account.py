from src.account import Account
class Account_personal(Account):
    express_outgoing_transfer_fee = 1.0
    def __init__(self, first_name:str, last_name:str, pesel:str, promo_code = None):
        self.balance=0.0
        self.first_name = first_name
        self.last_name = last_name
        self.pesel = pesel
        if type(pesel) != "string" and len(self.pesel) != 11:
            self.pesel = "Invalid"
        self.promo_code = promo_code
        if promo_code and len(promo_code)==8 and promo_code.startswith("PROM_") and yob_from_pesel(self.pesel)>1960:
            self.balance += 50
        self.history=[]

    def submit_for_loan(self, amount:float):
        length = len(self.history)
        if(length>=3) and self.history[-1]>0 and self.history[-2]>0 and self.history[-3]>0:
            self.balance+=amount
            return True  
        if length>=5 and self.history[-5]+self.history[-4]+self.history[-3]+self.history[-2]+self.history[-1]>amount:
            self.balance+=amount
            return True 
        else:
            return False

def yob_from_pesel(pesel): # dla roku 1900+
    if pesel.isdigit() : # isinstance(pesel, str) możnaby ale pesel jest już sprawdzany czy jest stringiem o długości 11
        if int(pesel[2:4]) > 12:
            return 2000 + int(pesel[:2])
        else:
            return 1900 + int(pesel[:2])
    else:
        return 0