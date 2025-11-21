from src.personal_account import  Account_personal

class AccountRegistry:
    def __init__(self):
        self.accounts:list[Account_personal] = []


    def add_account(self, account: Account_personal):
        self.accounts.append(account)

    def find_account_by_pesel(self, pesel:str):
        for account in self.accounts:
            if account.pesel == pesel:
                return account
        return None
        
    def return_all_accounts(self):
        return self.accounts

    def return_lenth_of_all_accounts(self):
        return len(self.accounts)
                

        