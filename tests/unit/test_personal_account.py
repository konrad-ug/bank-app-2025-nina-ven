from src.personal_account import  Account_personal
from src.personal_account import yob_from_pesel

class TestPersonalAccount:
    def test_account_creation(self):
        account = Account_personal("John", "Doe", "06211304545")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0.0
        assert account.pesel == "06211304545"

    def test_pesel_length(self):
        account = Account_personal("John", "Doe", "062113045")
        account2 = Account_personal("John", "Doe", "062244333113045")
        account3 = Account_personal("John", "Doe", "06211304545")
        assert account.pesel == "Invalid"
        assert account2.pesel == "Invalid"
        assert account3.pesel == "06211304545"


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
        account1 = Account_personal("John", "Doe", "59121304545", "PROM_XYZ")
        assert account1.history == []
        account1.transfer_in(100)
        assert account1.history == [100]
        account1.transfer_out(10)
        assert account1.history == [100,-10]
        account1.express_transfer_out(50)
        assert account1.history == [100,-10,-50,-1]

    def test_does_loan_work(self):
        account1 = Account_personal("John", "Doe", "59121304545")

        account1.history=[50.0,30.0,100.0]
        assert account1.submit_for_loan(30.0) == True
        assert account1.balance == 30.0

        account1.history=[50.0,30.0,100.0,-10.0,-10.0]
        assert account1.submit_for_loan(30.0) == True
        assert account1.balance == 60.0
        
    def test_does_loan_work_without_right_conditions(self):
        account1 = Account_personal("John", "Doe", "59121304545")

        assert account1.submit_for_loan(30.0) == False
        assert account1.balance == 0.0

        account1.history=[-5.0,-10.0,-20.0]
        assert account1.submit_for_loan(30.0) == False
        assert account1.balance == 0.0

        account1.history=[-5.0,-10.0,-20.0,10,10]
        assert account1.submit_for_loan(30.0) == False
        assert account1.balance == 0.0



