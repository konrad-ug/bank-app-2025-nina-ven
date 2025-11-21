from src.account_registry import AccountRegistry
from src.personal_account import  Account_personal
import pytest 

class TestAccountRegistry:

    @pytest.fixture(autouse=True)
    def registry(self):
        self.registry = AccountRegistry()

    @pytest.fixture(autouse=True)
    def account1(self):
        self.account1 = Account_personal("John", "Doe", "06211314545")

    
    @pytest.fixture(autouse=True)
    def account2(self):
        self.account2 = Account_personal("Jane", "Doe", "06230704545")


    def test_does_adding_to_registry_work(self):
        self.registry.add_account(self.account1)
        assert self.registry.accounts[-1] == self.account1
        
    def test_does_finding_account_bt_pesel_work(self):
        self.registry.accounts = [self.account1]
        assert self.registry.find_account_by_pesel("06211314545") == self.account1
        assert self.registry.find_account_by_pesel("07211304545") == None

    def test_does_returning_all_accounts_work(self):
        self.registry.accounts = [self.account1, self.account2]
        assert self.registry.return_all_accounts() == [self.account1, self.account2]
    
    def test_does_returning_length_of_all_accounts_work(self):
        self.registry.accounts = [self.account1, self.account2]
        assert self.registry.return_lenth_of_all_accounts() == 2

        