from src.account import Account


class TestAccount:
    def test_account_creation(self):
        account = Account("John", "Doe", '06211304545', 200.0)
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 200.0
        assert account.pesel == "06211304545"

    def test_pesel_length(self):
        account = Account("John", "Doe", '062113045', 200.0)
        account2 = Account("John", "Doe", '062244333113045', 200.0)
        assert account.pesel == "Invalid"
        assert account2.pesel == "Invalid"



    def test_is_code_correct_format(self):
        account = Account("John", "Doe", '062113045', 200.0, "AAA_aa")
        assert account.balance == 200



