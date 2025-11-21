from src import account
from src.company_account import  Account_company
import pytest 

class TestCompanyAccount:

    @pytest.fixture(autouse=True)
    def account(self):
        self.account = Account_company('biodem','2749373834')

    def test_does_invalid_nip_work(self):      
        assert self.account.nip == '2749373834'
        account2 = Account_company('biodem','2')
        assert account2.nip == 'Invalid'

    def test_does_history_work(self):
        assert self.account.history == []
        self.account.transfer_in(100)
        assert self.account.history == [100]
        self.account.transfer_out(10)
        assert self.account.history == [100,-10]
        self.account.express_transfer_out(50)
        assert self.account.history == [100,-10,-50,-5]

class TestLoan:

    @pytest.fixture(autouse=True)
    def account(self):
        self.account = Account_company('biodem','2749373834')

    @pytest.mark.parametrize("history, balance,  amount, expected_result, expected_balance",
    [
        ([50, -1775, -100], 60, 30, True, 90),
        ([-50, -100, -30], 200, 50, False, 200),
        ([-1775, -100, 30], 300, 3000, False, 300),
        ([700, -100, -20], 200, 1000, False, 200),
 
    ],
    ids=[
        "saldo >= than loan and transfer to ZUS",
        "saldo >= than loan no transfer to ZUS",
        "sald < than loan and transfet to ZUS",
        "sald < than and no transfet to ZUS"
    ])

    def test_loan(self, history, balance, amount, expected_result, expected_balance):
        self.account.history=history
        self.account.balance=balance
        result = self.account.submit_for_loan(amount)
        assert result == expected_result
        assert self.account.balance == expected_balance
        
