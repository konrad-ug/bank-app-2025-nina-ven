from src.personal_account import  Account_personal
from src.personal_account import yob_from_pesel
import pytest

class TestPersonalAccount:

    @pytest.fixture(autouse=True)
    def account(self):
        self.account = Account_personal("John", "Doe", "06211304545")

    def test_account_creation(self):
        assert self.account.first_name == "John"
        assert self.account.last_name == "Doe"
        assert self.account.balance == 0.0
        assert self.account.pesel == "06211304545"

    def test_pesel_length(self):
        account = Account_personal("John", "Doe", "062113045")
        account2 = Account_personal("John", "Doe", "062244333113045")
        assert account.pesel == "Invalid"
        assert account2.pesel == "Invalid"


    def test_is_code_correct_format(self):
        account1 = Account_personal("John", "Doe", "06211304545", "AAA_aa")
        account2 = Account_personal("John", "Doe", "06211304545", "aa")
        account3 = Account_personal("John", "Doe", "06211304545", "PROM_aa")
        account4 = Account_personal("John", "Doe", "06211304545", "prom_xyz")
        assert account1.balance == 0.0
        assert account2.balance == 0.0
        assert account3.balance == 0.0
        assert account4.balance == 0.0

    def test_does_code_work(self):
        account = Account_personal("John", "Doe", "06211304545", "PROM_XYZ")
        assert account.balance == 50.0

    def test_yob_function(self):
        assert yob_from_pesel("06211304545") == 2006
        assert yob_from_pesel("Invalid") == 0
        assert yob_from_pesel("81121304545") == 1981

    def test_does_code_work_for_seniors(self):
        account1 = Account_personal("John", "Doe", "59121304545", "PROM_XYZ")
        account2 = Account_personal("John", "Doe", "20121304545", "PROM_XYZ")
        assert account1.balance == 0.0
        assert account2.balance == 0.0

    def test_does_history_work(self):
        assert self.account.history == []
        self.account.transfer_in(100)
        assert self.account.history == [100]
        self.account.transfer_out(10)
        assert self.account.history == [100,-10]
        self.account.express_transfer_out(50)
        assert self.account.history == [100,-10,-50,-1]

    @pytest.mark.parametrize("history, amount, expected_result, expected_balance",
    [
    ([50,30,100],30,True,30),
    ([50.0,30.0,100.0,-10.0,-10.0],30,True,30),
    ([40],30,False,0),
    ([5.0,10.0,-20.0],30,False,0),
    ([-5.0,-10.0,-20.0,10,10],30,False,0)
    ],
    ids=[
        "three positives",
        "five with sum greater than 0",
        "one positive",
        "three but one is negative",
        "five with sum lesser than 0"
    ])

    def test_loan(self, history, amount, expected_result, expected_balance):
        self.account.history=history
        result = self.account.submit_for_loan(amount)
        assert result == expected_result
        assert self.account.balance == expected_balance

    # def test_does_loan_work(self):

    #     self.account.history=[50.0,30.0,100.0]
    #     assert self.account.submit_for_loan(30.0) == True
    #     assert self.account.balance == 30.0

    #     self.account.history=[50.0,30.0,100.0,-10.0,-10.0]
    #     assert self.account.submit_for_loan(30.0) == True
    #     assert self.account.balance == 60.0
        
    # def test_does_loan_work_without_right_conditions(self):

    #     assert self.account.submit_for_loan(30.0) == False
    #     assert self.account.balance == 0.0

    #     self.account.history=[5.0,10.0,-20.0]
    #     assert self.account.submit_for_loan(30.0) == False
    #     assert self.account.balance == 0.0

    #     self.account.history=[-5.0,-10.0,-20.0,10,10]
    #     assert self.account.submit_for_loan(30.0) == False
    #     assert self.account.balance == 0.0



