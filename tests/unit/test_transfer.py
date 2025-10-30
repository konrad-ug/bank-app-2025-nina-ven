from src.account import Account

class TestTransfer:
    def test_does_transfer_in_transfer_money(self):
        account1 = Account("John", "Doe", "06211304545", 200.0)
        account1.transfer_in(50.0)
        assert account1.balance == 250

    def test_does_transfer_out_transfer_money(self):
        account1 = Account("John", "Doe", "06211304545", 200.0)
        account1.transfer_out(50.0)
        assert account1.balance == 150

    def test_does_transfer_with_too_much_money_work(self):
        account1 = Account("John", "Doe", "06211304545", 200.0)
        assert account1.transfer_out(500.0) == "Brak fundów do transferu"
        assert account1.balance == 200
