import datetime
import pytest

from src.personal_account import Account_personal
from src.company_account import Account_company

class TestEmailPersonal:
    today_date = datetime.datetime.today().strftime('%Y-%m-%d')

    def test_send_history_via_email_personal_account(self, mocker):
        account = Account_personal("John", "Doe", "06211304545")

        account.history = [150.0, -50.0]

        mock_send = mocker.patch('src.personal_account.SMTPClient.send', return_value=True)

        result = account.send_history_via_email("pers@test.com")

        assert result is True
        mock_send.assert_called_once()

        subject = mock_send.call_args[0][0]
        text = mock_send.call_args[0][1]
        email_address = mock_send.call_args[0][2]

        assert subject == "Account Transfer History " + self.today_date
        assert email_address == "pers@test.com"
        assert text == f"Personal account history: {account.history}"

    def test_send_history_via_email_personal_account_failed(self, mocker):
        account = Account_personal("Jane", "Smith", "98765432101")
        account.history = [150.0, -50.0]

        mock_send = mocker.patch('src.personal_account.SMTPClient.send', return_value=False)

        result = account.send_history_via_email("pers@test.com")

        assert result is False

class TestEmailCompany:
    today_date = datetime.datetime.today().strftime('%Y-%m-%d')

    @pytest.fixture(autouse=True)
    def _mock_verify_nip(self, mocker):
        mocker.patch("src.company_account.Account_company.is_nip_active_in_MF_registry", return_value=True)

    def test_send_history_via_email_company_account_success(self, mocker):
        account = Account_company("biodem","8461627562")
        account.history = [50.0, 100, 300, 100]

        mock_send = mocker.patch("src.company_account.SMTPClient.send", return_value=True)

        result = account.send_history_via_email("corp@test.com")

        assert result is True
        mock_send.assert_called_once()

        subject, text, email = mock_send.call_args[0]

        assert subject == f"Account Transfer History {self.today_date}"
        assert text == f"Company account history: {account.history}"
        assert email == "corp@test.com"

    def test_send_history_via_email_company_account_failed(self, mocker):
        account = Account_company("biodem","8461627562")
        account.history = [10, -10]

        mocker.patch("src.company_account.SMTPClient.send", return_value=False)

        result = account.send_history_via_email("corp@test.com")

        assert result is False