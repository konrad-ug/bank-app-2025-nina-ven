from http.client import responses

import pytest
import requests

class TestTransfer:

    @pytest.fixture(autouse=True, scope="function")
    def setup_method(self):
        url = "http://localhost:5000/api/accounts"
        response = requests.post(url, json={
            "name": "Jane",
            "surname": "Doe",
            "pesel": "06210802343"
        })
        assert response.status_code == 201
        response = requests.post(f"{url}/06210802343/transfer", json={"amount": 500,"type": "incoming"})
        assert response.status_code==200
        yield
        response = requests.get(url)
        accounts = response.json()
        for account in accounts:
            pesel = account["pesel"]
            requests.delete(f"{url}/{pesel}")

    @pytest.fixture(autouse=True)
    def person(self):
        self.person = {
            "name": "Jane",
            "surname": "Doe",
            "pesel": "06210802343"
        }

    @pytest.fixture(autouse=True)
    def url(self):
        self.url = "http://localhost:5000/api/accounts"

    @pytest.mark.parametrize("body, status, message",
    [
        [{"amount": 100, "type": "incoming"}, 200, "The request has been accepted for processing"],
        [{"amount": 500, "type": "outgoing"}, 200, "The request has been accepted for processing"],
        [{"amount": 800, "type": "outgoing"}, 422, "Transfer did not go through - Not enough funds"],
        [{"amount": 300, "type": "express"}, 200, "The request has been accepted for processing"],
        [{"amount": 600, "type": "express"}, 422, "Transfer did not go through - Not enough funds"],
        [{"amount": 110, "type": "fun_one"}, 422, "Type does not exist"]
    ],
    ids=[
        "transfer in",
        "transfer out",
        "transfer out without enough funds",
        "express transfer out",
        "express transfer out without enough funds",
        "incorrect type of transfer"

    ])

    def test_transfer_on_existing_account(self, body, status, message):
        response = requests.post(f"{self.url}/06210802343/transfer", json=body)
        assert response.status_code == status
        assert response.json()["message"] == message

    def test_does_transfer_for_nonexistent_account_work(self):
        response = requests.post(f"{self.url}/09251002342/transfer", json={"amount": 500, "type": "incoming"})
        assert response.status_code == 404
        assert response.json()["message"] == "Account not found"


    # def test_does_transfer_in_work(self):
    #     response = requests.post(f"{self.url}/06210802343/transfer", json={"amount": 100,"type": "incoming"})
    #     assert response.status_code == 200
    #     assert response.json()["message"] == "The request has been accepted for processing"
    #
    # def test_does_transfer_out_work(self):
    #     response = requests.post(f"{self.url}/06210802343/transfer", json={"amount": 500, "type": "outgoing"})
    #     assert response.status_code == 200
    #     assert response.json()["message"] == "The request has been accepted for processing"
    #
    # def test_does_express_transfer_work(self):
    #     response = requests.post(f"{self.url}/06210802343/transfer", json={"amount": 300, "type": "express"})
    #     assert response.status_code == 200
    #     assert response.json()["message"] == "The request has been accepted for processing"
    #
    # def test_too_large_transfer_out_work(self):
    #     response = requests.post(f"{self.url}/06210802343/transfer", json={"amount": 600, "type": "express"})
    #     assert response.status_code == 422
    #     assert response.json()["message"] == "Transfer did not go through - Not enough funds"
    #
    #     response = requests.post(f"{self.url}/06210802343/transfer", json={"amount": 800, "type": "outgoing"})
    #     assert response.status_code == 422
    #     assert response.json()["message"] == "Transfer did not go through - Not enough funds"

    # def test_does_transfer_of_unknown_type_not_work(self):
    #     response = requests.post(f"{self.url}/06210802343/transfer", json={"amount": 500, "type": "fun"})
    #     assert response.status_code == 422
    #     assert response.json()["message"] == "Type does not exist"