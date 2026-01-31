from datetime import datetime
import os
import requests
from src.account import Account

class Account_company(Account):
    express_outgoing_transfer_fee = 5.0
    bank_url = os.getenv("BANK_APP_MF_URL", "https://wl-api.mf.gov.pl/")
    def __init__(self, company_name:str, nip:str):
        super().__init__()
        self.company_name = company_name
        self.history:list[float] = []
        self.balance:float = 0.0

        if not self.is_nip_valid(nip):
            self.nip= "Invalid"
        elif self.is_nip_active_in_MF_registry(nip):
            self.nip=nip
        else:
            raise ValueError("NIP is not active in MF registry")

    def is_nip_valid(self,nip):
        if isinstance(nip, str) and len(nip) == 10  and nip.isdigit():
            return True
        return False


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

    def is_nip_active_in_MF_registry(self, nip) -> bool :
        today_date=datetime.today().strftime('%Y-%m-%d')
        url = f'{self.bank_url}api/search/nip/{nip}?date={today_date}'
        print(f"sending requests to {url}")
        response=requests.get(url)
        print(f"Response status code: {response.json()}")
        if response.status_code != 200:
            return False
        data = response.json() or {}
        result = data.get("result") or {}
        subject = result.get("subject") or {}
        status = subject.get("statusVat")

        return status == "Czynny"