from src.company_account import  Account_company
import pytest

class TestCompanyAccount:


    def test_company_account_creation(self,mocker):
        mock = mocker.patch("src.company_account.requests.get")
        mock.return_value.status_code = 200
        mock.return_value.json.return_value = {
            "result": {"subject": {"statusVat": "Czynny"}}
        }
        account = Account_company("biodem","8461627562")
        assert account.company_name == "biodem"
        assert account.balance == 0
        assert account.nip == '8461627562'

    def test_nip_wrong_length(self,mocker):
        mock_get = mocker.patch("src.company_account.requests.get")
        account=Account_company("biodem","111111111111111111")
        assert account.nip == "Invalid"
        account=Account_company("biodem","1")
        assert account.nip == "Invalid"
        mock_get.assert_not_called()

    def test_nip_nondigit(self,mocker):
        mock_get = mocker.patch("src.company_account.requests.get")
        account = Account_company("biodem", "aaa")
        assert account.nip == "Invalid"
        mock_get.assert_not_called()

    def test_inactive_company(self, mocker):
        mock = mocker.patch("src.company_account.requests.get")
        mock.return_value.status_code = 200
        mock.return_value.json.return_value = {
            "result": {"subject": {"statusVat": "Zwolniony"}}
        }

        with pytest.raises(ValueError):
            Account_company("biodem", "8461627562")

    def test_nip_api_returns_no_data(self, mocker):
        mock = mocker.patch("src.company_account.requests.get")
        mock.return_value.status_code = 200
        mock.return_value.json.return_value = {}

        account = Account_company("biodem", "8461627562")
        assert account.nip == "8461627562"

    def test_nip_api_returns_non_200(self, mocker):
        mock = mocker.patch("src.company_account.requests.get")
        mock.return_value.status_code = 500
        mock.return_value.json.return_value = {}

        account = Account_company("biodem", "8461627562")
        assert account.nip == "8461627562"



    def test_does_history_work(self,mocker):
        mock = mocker.patch("src.company_account.requests.get")
        mock.return_value.status_code = 200
        mock.return_value.json.return_value = {
            "result": {"subject": {"statusVat": "Czynny"}}
        }
        account = Account_company("biodem", "8461627562")
        assert account.history == []
        account.transfer_in(100)
        assert account.history == [100]
        account.transfer_out(10)
        assert account.history == [100,-10]
        account.express_transfer_out(50)
        assert account.history == [100,-10,-50,-5]

class TestLoan:

    @pytest.fixture(autouse=True)
    def account(self,mocker):
        mocker.patch(
            "src.company_account.Account_company.is_nip_active_in_MF_registry",
            return_value=True
        )
        self.account = Account_company('biodem','8461627562')

    @pytest.mark.parametrize("history, balance,  amount, expected_result, expected_balance",
    [
        ([50, -1775, -100], 60, 30, True, 90),
        ([-50, -100, -30], 200, 50, False, 200),
        ([-1775, -100, 30], 300, 3000, False, 300),
        ([700, -100, -20], 200, 1000, False, 200),
 
    ],
    ids=[
        "saldo >= than loan and transfer to ZUS",
        "saldo >= than loan no transfer to ZUS",
        "sald < than loan and transfet to ZUS",
        "sald < than and no transfet to ZUS"
    ])

    def test_loan(self, history, balance, amount, expected_result, expected_balance):
        self.account.history=history
        self.account.balance=balance
        result = self.account.submit_for_loan(amount)
        assert result == expected_result
        assert self.account.balance == expected_balance
        
