from src.account import Account
from src.company_account import  Account_company
from src.personal_account import  Account_personal
import pytest

class TestTransfer:
    @pytest.fixture(autouse=True)
    def account(self):
        self.account = Account()

    def test_does_transfer_in_transfer_money(self):
        self.account.transfer_in(50.0)
        assert self.account.balance == 50

    def test_does_transfer_out_transfer_money(self):
        self.account.balance=200
        self.account.transfer_out(50.0)
        assert self.account.balance == 150

    def test_does_transfer_with_too_much_money_work(self):
        self.account.transfer_out(50.0)
        assert self.account.balance == 0

class Test_express_transfer_personal:

    @pytest.fixture(autouse=True)
    def account(self):
        self.account = Account_personal("John", "Doe", "06211304545")
        
    def test_does_transfer_out_transfer_money(self):
        self.account.balance=200.0
        self.account.express_transfer_out(50)
        assert self.account.balance == 149

    def test_does_transfer_with_too_much_money_work(self):
        self.account.balance=200.0
        self.account.express_transfer_out(201)
        assert self.account.balance == 200

    def test_does_transfer_with_all_money_work(self):
        self.account.balance=200.0
        self.account.express_transfer_out(200)
        assert self.account.balance == -1

class Test_express_transfer_company:

    @pytest.fixture(autouse=True)
    def account(self):
        self.account = Account_company('biodem','2749373834')
    
    def test_does_transfer_out_transfer_money(self):
        self.account.balance=200.0
        self.account.express_transfer_out(50)
        assert self.account.balance == 145

    def test_does_transfer_with_too_much_money_work(self):
        self.account.balance=200.0
        self.account.express_transfer_out(201)
        assert self.account.balance == 200

    def test_does_transfer_with_all_money_work(self):
        self.account.balance=200.0
        self.account.express_transfer_out(200)
        assert self.account.balance == -5

