import requests
import pytest

class Test_time:

    @pytest.fixture(autouse=True, scope="function")
    def setup_method(self):
        url = "http://localhost:5000/api/accounts"
        response = requests.get(url)
        accounts = response.json()
        for account in accounts:
            pesel = account["pesel"]
            requests.delete(f"{url}/{pesel}")
        assert response.status_code == 200
        yield


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

    @pytest.fixture(autouse=True)
    def time(self):
        self.time = 0.5

    @pytest.fixture(autouse=True)
    def amount(self):
        self.amount = 100

    def test_time_of_creation_and_deletion(self):
        for _ in range(self.amount):
            response = requests.post(self.url, json=self.person, timeout=self.time)
            assert response.status_code == 201
            response = requests.delete(f"{self.url}/{self.person['pesel']}", timeout=self.time)
            assert response.status_code == 200

    def test_time_of_logging_transfers(self):
        response = requests.post(self.url, json=self.person)
        assert response.status_code == 201
        for _ in range(self.amount):
            response = requests.post(f"{self.url}/{self.person['pesel']}/transfer", json={"amount": 1, "type": "incoming"}, timeout=self.time)
            assert response.status_code == 200
        response = requests.get(f"{self.url}/{self.person['pesel']}")
        assert response.status_code == 200
        assert response.json()["balance"] == self.amount*1
        response = requests.delete(f"{self.url}/{self.person['pesel']}")
        assert response.status_code == 200



