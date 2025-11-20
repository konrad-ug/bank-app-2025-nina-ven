from src.account import Account
class Account_personal(Account):
    express_outgoing_transfer_fee = 1.0
    def __init__(self, first_name:str, last_name:str, pesel:str, promo_code = None):
        self.balance=0.0
        self.first_name = first_name
        self.last_name = last_name
        self.pesel = pesel
        if len(self.pesel) != 11:
            self.pesel = "Invalid"
        self.promo_code = promo_code
        if promo_code and self.is_promo_code_correct():
            self.balance += 50
        self.history=[]

    def yob_from_pesel(self): # dla roku 1900+
        if self.pesel.isdigit() : 
            if int(self.pesel[2:4]) > 12:
                return 2000 + int(self.pesel[:2])
            else:
                return 1900 + int(self.pesel[:2])
        else:
            return 0
        
    def is_promo_code_correct(self):
        if len(self.promo_code)==8 and self.promo_code.startswith("PROM_") and self.yob_from_pesel()>1960:
            return True
        else:
            return False

    def submit_for_loan(self, amount:float):
        length = len(self.history)
        if(length>=3) and self.check_positivity_of_last_three():
            self.balance+=amount
            return True  
        if length>=5 and self.check_positivity_of_sum_of_last_five(amount):
            self.balance+=amount
            return True 
        else:
            return False
        
    def check_positivity_of_last_three(self):
        if self.history[-1]>0 and self.history[-2]>0 and self.history[-3]>0:
            return True
        else:
            return False
        
    def check_positivity_of_sum_of_last_five(self,amount):
        if self.history[-5]+self.history[-4]+self.history[-3]+self.history[-2]+self.history[-1]>amount:
            return True
        else:
            return False

