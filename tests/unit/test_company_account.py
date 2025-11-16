from src.company_account import  Account_company

class TestCompanyAccount:
    def test_does_invalid_nip_work(self):
        account1 = Account_company('biodem', '2749373834')
        assert account1.nip == '2749373834'
        account2 = Account_company('biodem', '279373834')
        assert account2.nip == 'Invalid'

    def test_does_history_work(self):
        account1 = Account_company('biodem', '2749373834')
        assert account1.history == []
        account1.transfer_in(100)
        assert account1.history == [100]
        account1.transfer_out(10)
        assert account1.history == [100,-10]
        account1.express_transfer_out(50)
        assert account1.history == [100,-10,-50,-5]
        
