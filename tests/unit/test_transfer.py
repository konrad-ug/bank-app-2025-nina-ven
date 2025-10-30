from src.account import Account
from src.company_account import  Account_company
from src.personal_account import  Account_personal

class TestTransfer:
    def test_does_transfer_in_transfer_money(self):
        account1 = Account()
        account1.transfer_in(50.0)
        assert account1.balance == 50

    def test_does_transfer_out_transfer_money(self):
        account1 = Account()
        account1.balance=200
        account1.transfer_out(50.0)
        assert account1.balance == 150

    def test_does_transfer_with_too_much_money_work(self):
        account1 = Account()
        assert account1.balance == 0

class Test_express_transfer_personal:
    def test_does_transfer_out_transfer_money(self):
        account1 = Account_personal("John", "Doe", "06211304545", 200.0)
        account1.express_transfer_out(50)
        assert account1.balance == 149

    def test_does_transfer_with_too_much_money_work(self):
        account1 = Account_personal("John", "Doe", "06211304545", 200.0)
        account1.express_transfer_out(201)
        assert account1.balance == 200

    def test_does_transfer_with_all_money_work(self):
        account1 = Account_personal("John", "Doe", "06211304545", 200.0)
        account1.express_transfer_out(200)
        assert account1.balance == -1

class Test_express_transfer_company:
    def test_does_transfer_out_transfer_money(self):
        account1 = Account_company('biodem', '2749373834',200)
        account1.express_transfer_out(50)
        assert account1.balance == 145

    def test_does_transfer_with_too_much_money_work(self):
        account1 = Account_company('biodem', '2749373834',200)
        account1.express_transfer_out(201)
        assert account1.balance == 200

    def test_does_transfer_with_all_money_work(self):
        account1 = Account_company('biodem', '2749373834',200)
        account1.express_transfer_out(200)
        assert account1.balance == -5

