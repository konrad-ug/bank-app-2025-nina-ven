from src.company_account import  Account_company

class TestCompanyAccount:
    def test_does_invalid_nip_work(self):
        account1 = Account_company('biodem', '2749373834')
        assert account1.nip == '2749373834'
        account2 = Account_company('biodem', '279373834')
        assert account2.nip == 'Invalid'
