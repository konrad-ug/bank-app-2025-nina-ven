from src.personal_account import  Account_personal
from src.personal_account import yob_from_pesel

class TestPersonalAccount:
    def test_account_creation(self):
        account = Account_personal("John", "Doe", "06211304545", 200.0)
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 200.0
        assert account.pesel == "06211304545"

    def test_pesel_length(self):
        account = Account_personal("John", "Doe", "062113045", 200.0)
        account2 = Account_personal("John", "Doe", "062244333113045", 200.0)
        account3 = Account_personal("John", "Doe", "06211304545", 200.0)
        assert account.pesel == "Invalid"
        assert account2.pesel == "Invalid"
        assert account3.pesel == "06211304545"


    def test_is_code_correct_format(self):
        account1 = Account_personal("John", "Doe", "06211304545", 200.0, "AAA_aa")
        account2 = Account_personal("John", "Doe", "06211304545", 200.0, "aa")
        account3 = Account_personal("John", "Doe", "06211304545", 200.0, "PROM_aa")
        account4 = Account_personal("John", "Doe", "06211304545", 200.0, "prom_xyz")
        assert account1.balance == 200
        assert account2.balance == 200
        assert account3.balance == 200
        assert account4.balance == 200

    def test_does_code_work(self):
        account = Account_personal("John", "Doe", "06211304545", 200.0, "PROM_XYZ")
        assert account.balance == 250

    def test_yob_function(self):
        assert yob_from_pesel("06211304545") == 2006
        assert yob_from_pesel("Invalid") == 0
        assert yob_from_pesel("81121304545") == 1981

    def test_does_code_work_for_seniors(self):
        account1 = Account_personal("John", "Doe", "59121304545", 200.0, "PROM_XYZ")
        account2 = Account_personal("John", "Doe", "20121304545", 200.0, "PROM_XYZ")
        assert account1.balance == 200
        assert account2.balance == 200




