import pytest
import requests

class TestAPI:

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


    def test_create_account(self):
        response = requests.post(self.url, json=self.person)
        assert response.status_code == 201
        assert response.json()["message"]== "Account created"

    def test_get_all_accounts(self):
        response=requests.get(self.url)
        assert response.status_code == 200
        assert response.json() == [{"name": "Jane", "surname": "Doe", "pesel":"06210802343", "balance":0.0}]

    def test_get_account_count(self):
        response=requests.get(f"{self.url}/count")
        assert response.status_code == 200
        assert response.json()["count"]==1

    def test_get_account_by_pesel(self):
        response=requests.get(f"{self.url}/06210802343")
        assert response.status_code == 200
        assert response.json() == [{"name": "Jane", "surname": "Doe", "pesel": "06210802343", "balance": 0.0}]

    def test_get_account_by_nonexistent_pesel(self):
        response = requests.get(f"{self.url}/05301009823")
        assert response.status_code == 404
        assert response.json()["message"] == "Account not found"

    def test_update_account(self):
        response = requests.patch(f"{self.url}/06210802343", json = {"name": "Alyssa"})
        assert response.status_code == 200
        assert response.json()["message"] == "Account updated"
        response2 = requests.get(f"{self.url}/06210802343")
        assert response2.json()["name"] == "Alyssa"
        assert response2.json()["surname"] == "Doe"


    def test_delete_account(self):
        response = requests.delete(f"{self.url}/06210802343")
        assert response.status_code == 200
        assert response.json()["message"] == "Account deleted"
        response2 = requests.get(f"{self.url}/06210802343")
        assert response2.status_code == 404







