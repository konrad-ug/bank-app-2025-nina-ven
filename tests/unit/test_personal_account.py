from src.personal_account import  Account_personal
import pytest

class TestPersonalAccount:

    @pytest.fixture(autouse=True)
    def account(self):
        self.account = Account_personal("John", "Doe", "06211304545")

    def test_account_creation(self):
        assert self.account.first_name == "John"
        assert self.account.last_name == "Doe"
        assert self.account.pesel == "06211304545"

    def test_pesel_length(self):
        account = Account_personal("John", "Doe", "062113045")
        account2 = Account_personal("John", "Doe", "062244333113045")
        assert account.pesel == "Invalid"
        assert account2.pesel == "Invalid"

    def test_does_history_work(self):
        assert self.account.history == []
        self.account.transfer_in(100)
        assert self.account.history == [100]
        self.account.transfer_out(10)
        assert self.account.history == [100,-10]
        self.account.express_transfer_out(50)
        assert self.account.history == [100,-10,-50,-1]

class TestPromoCode:

    @pytest.mark.parametrize("first_name, last_name, pesel, promo_code, expected_balance",
    [
        ["John", "Doe", "06211304545","PROM_XYZ", 50],
        ["John", "Doe", "06211304545","aa", 0],
        ["John", "Doe", "06211304545","prom_xyz", 0],
        ["John", "Doe", "06211304545","AAA_aaa", 0],
        ["John", "Doe", "06211304545","PROM_aa", 0],
        ["John", "Doe", "59121304545","PROM_XYZ", 0],
    ],
    ids=[
        "correct promo code",
        "everything wrong",
        "starts with right letters but not in caps right length",
        "starts in wrong letters in caps right lenght",
        "starts in right letters in caps wrong length",
        "right code but senior user"
    ])

    def test_creating_accounts_with_promo_code(self, first_name, last_name, pesel, promo_code, expected_balance):
        account = Account_personal(first_name, last_name, pesel, promo_code)
        assert account.balance == expected_balance

class TestYob:

    @pytest.mark.parametrize("first_name, last_name, pesel, expected_year",
    [
        ["John", "Doe", "06211304545",2006],
        ["John", "Doe", "222",0],
        ["John", "Doe", "81121304545",1981]
    ],
    ids=[
        "someone born during 21st century",
        "someone with incorrect pesel",
        "someone born during 20th century"
    ])

    def test_yob_function(self, first_name, last_name, pesel, expected_year):
        account = Account_personal(first_name, last_name, pesel)
        assert account.yob_from_pesel() == expected_year


class TestLoan:

    @pytest.fixture(autouse=True)
    def account(self):
        self.account = Account_personal("John", "Doe", "06211304545")

    @pytest.mark.parametrize("history, amount, expected_result, expected_balance",
    [
        ([50,30,100], 30, True, 30),
        ([50.0,30.0,100.0,-10.0,-10.0], 30, True, 30),
        ([40], 30, False, 0),
        ([5.0,10.0,-20.0], 30, False, 0),
        ([-5.0,-10.0,-20.0,10,10], 30, False, 0)
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





