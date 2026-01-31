import pytest
from src.account import Account
from src.account_repository import MongoAccountsRepository
from src.personal_account import Account_personal


class TestMongoRepository:
    def test_save_all(self, mocker):

        mock_collection = mocker.MagicMock()
        mock_db = mocker.MagicMock()
        mock_db.__getitem__.return_value = mock_collection
        mock_client_instance = mocker.MagicMock()
        mock_client_instance.__getitem__.return_value = mock_db


        mocker.patch('src.account_repository.MongoClient', return_value=mock_client_instance)

        repo = MongoAccountsRepository()

        acc1 = Account_personal("John", "Doe", "06211304545")
        acc2 = Account_personal("Jane", "Doe", "05211304545")
        accounts = [acc1, acc2]

        repo.save_all(accounts)

        mock_collection.delete_many.assert_called_once_with({})
        assert mock_collection.insert_one.call_count == 2

    def test_load_all(self, mocker):
        mock_collection = mocker.MagicMock()
        fake_data = [
            {
                "first_name": "John",
                "last_name": "Doe",
                "pesel": "06211304545",
                "balance": 300.0,
                "transfers": [300],
                "promo_code": None,
                "type": "personal"
            }
        ]
        mock_collection.find.return_value = fake_data

        mock_db = mocker.MagicMock()
        mock_db.__getitem__.return_value = mock_collection

        mock_client_instance = mocker.MagicMock()
        mock_client_instance.__getitem__.return_value = mock_db

        mocker.patch('src.account_repository.MongoClient', return_value=mock_client_instance)

        repo = MongoAccountsRepository()
        loaded = repo.load_all()

        assert len(loaded) == 1
        assert loaded[0].first_name == "John"
        assert loaded[0].balance == 300.0

    def test_load_all_business_account(self, mocker):
        mock_collection = mocker.MagicMock()
        fake_data = [
            {
                "company_name": "biodem",
                "nip": '8461627562',
                "balance": 5000.0,
                "transfers": [5000],
                "type": "business"
            }
        ]
        mock_collection.find.return_value = fake_data

        mock_db = mocker.MagicMock()
        mock_db.__getitem__.return_value = mock_collection

        mock_client_instance = mocker.MagicMock()
        mock_client_instance.__getitem__.return_value = mock_db

        mocker.patch('src.account_repository.MongoClient', return_value=mock_client_instance)

        repo = MongoAccountsRepository()
        loaded = repo.load_all()

        assert len(loaded) == 1
        assert loaded[0].balance == 5000.0
        assert loaded[0].nip == '8461627562'

    def test_load_all_invalid_business_account(self, mocker):
        mock_collection = mocker.MagicMock()
        fake_data = [
            {
                "company_name": None,
                "nip": "11",
                "balance": 0.0,
                "transfers": [],
                "type": "business"
            }
        ]
        mock_collection.find.return_value = fake_data

        mock_db = mocker.MagicMock()
        mock_db.__getitem__.return_value = mock_collection

        mock_client_instance = mocker.MagicMock()
        mock_client_instance.__getitem__.return_value = mock_db

        mocker.patch('src.account_repository.MongoClient', return_value=mock_client_instance)

        repo = MongoAccountsRepository()
        loaded = repo.load_all()

        assert loaded == []