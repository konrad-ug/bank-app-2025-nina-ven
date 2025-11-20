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

    # @pytest.mark.parametrize("balance, amount, expected_balance",
    # [
    #     [200,50,150],
    #     [100,1000,100],
    # ],
    # ids=[
    #     "less money transfered than owned",
    #     "more money transfered than owned",
    # ])   

    # def test_transfer_out(self, balance, amount, expected_balance):
    #     self.account.balance=balance
    #     self.account.transfer_out(amount)
    #     assert self.account.balance == expected_balance

class Test_express_transfer_personal:

    @pytest.fixture(autouse=True)
    def account(self):
        self.account = Account_personal("John", "Doe", "06211304545")

    @pytest.mark.parametrize("balance, amount, expected_balance",
    [
        [100,50,49],
        [100,300,100],
        [400,400,-1]
    ],
    ids=[
        "less money transfered than owned",
        "more money transfered than owned",
        "money transfered and owned are equal"
    ])   

    def test_express_transfer_personal(self, balance, amount, expected_balance):
        self.account.balance=balance
        self.account.express_transfer_out(amount)
        assert self.account.balance == expected_balance


class Test_express_transfer_company:

    @pytest.fixture(autouse=True)
    def account(self):
        self.account = Account_company('biodem','2749373834')

    @pytest.mark.parametrize("balance, amount, expected_balance",
    [
        [100,50,45],
        [100,300,100],
        [400,400,-5]
    ],
    ids=[
        "less money transfered than owned",
        "more money transfered than owned",
        "money transfered and owned are equal"
    ])   

    def test_express_transfer_company(self, balance, amount, expected_balance):
        self.account.balance=balance
        self.account.express_transfer_out(amount)
        assert self.account.balance == expected_balance

    


