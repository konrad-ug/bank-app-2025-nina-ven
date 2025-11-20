from src import account
from src.company_account import  Account_company
import pytest 

class TestCompanyAccount:

    @pytest.fixture(autouse=True)
    def account(self):
        self.account = Account_company('biodem','2749373834')

    def test_does_invalid_nip_work(self):      
        assert self.account.nip == '2749373834'
        account2=Account_company('biodem','2')
        assert account2.nip == 'Invalid'

    def test_does_history_work(self):
        assert self.account.history == []
        self.account.transfer_in(100)
        assert self.account.history == [100]
        self.account.transfer_out(10)
        assert self.account.history == [100,-10]
        self.account.express_transfer_out(50)
        assert self.account.history == [100,-10,-50,-5]
        
