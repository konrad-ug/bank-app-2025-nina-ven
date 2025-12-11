from flask import Flask, request, jsonify, abort
from src.account_registry import AccountRegistry
from src.personal_account import Account_personal

app = Flask(__name__)
registry = AccountRegistry()

@app.route("/api/accounts", methods=['POST'])
def create_account():
    data = request.get_json()
    print(f"Create account request: {data}")
    account = Account_personal(data("name"), data("surname"), data("pesel"))
    registry.add_account(account)
    return jsonify({"message": "Account created"}), 201

@app.route("/api/accounts", methods=['GET'])
def get_all_accounts():
    print("Get all accounts request recieved")
    accounts = registry.return_all_accounts()
    accounts_data = [{"name": acc.first_name, "surname": acc.last_name, "pesel":acc.pesel, "balance":acc.balance} for acc in accounts]
    return jsonify(accounts_data), 200

@app.route("/api/accounts/count", methods=['GET'])
def get_account_count():
    print("Get account count request recieved")
    count = registry.return_lenth_of_all_accounts()
    return jsonify({"count": count}), 200

@app.route("/api/accounts/<pesel>", methods=['GET'])
def get_account_by_pesel(pesel):
    print("Get account with pesel recieved")
    account = registry.find_account_by_pesel(pesel)
    if not account:
        return jsonify({"message": "Account not found"}), 404
    account_data = {"name":account.first_name, "surname":account.last_name, "pesel":account.pesel, "balance":account.balance}
    return jsonify(account_data), 200


@app.route("/api/accounts/<pesel>", methods=['PATCH'])
def update_account(pesel):
    account = registry.find_account_by_pesel(pesel)
    if not account:
        return jsonify({"message": "Account not found"}), 404
    data = request.get_json()
    if "name" in data:
        account.first_name = data["name"]
    if "surname" in data:
        account.last_name = data["surname"]
    return jsonify({"message": "Account updated"}), 200

@app.route("/api/accounts/<pesel>", methods=['DELETE'])
def delete_account(pesel):
    account=get_account_by_pesel(pesel)
    if not account:
        return jsonify({"message": "Account not found"}), 404
    registry.delete_account_by_pesel(pesel)
    return jsonify({"message": "Account deleted"}), 200
