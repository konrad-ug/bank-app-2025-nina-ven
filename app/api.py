from flask import Flask, request, jsonify, abort
from src.account_registry import AccountRegistry
from src.personal_account import Account_personal

app = Flask(__name__)
registry = AccountRegistry()

@app.route("/api/accounts", methods=['POST'])
def create_account():
    data = request.get_json()
    print("Create account request recieved")
    print(f"Create account request: {data}")
    if registry.find_account_by_pesel(data["pesel"]):
        return jsonify({"message": "Account of such pesel already exists"}), 409
    account = Account_personal(data["name"], data["surname"], data["pesel"])
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
    count = registry.return_length_of_all_accounts()
    return jsonify({"count": count}), 200

@app.route("/api/accounts/<pesel>", methods=['GET'])
def get_account_by_pesel(pesel):
    print("Get account by pesel recieved")
    account = registry.find_account_by_pesel(pesel)
    if not account:
        return jsonify({"message": "Account not found"}), 404
    account_data = {"name":account.first_name, "surname":account.last_name, "pesel":account.pesel, "balance":account.balance}
    return jsonify(account_data), 200

@app.route("/api/accounts/<pesel>", methods=['PATCH'])
def update_account(pesel):
    data = request.get_json()
    print("Update account recieved")
    print(f"Update account request: {data}")
    account = registry.find_account_by_pesel(pesel)
    if not account:
        return jsonify({"message": "Account not found"}), 404
    if "name" in data:
        account.first_name = data["name"]
    if "surname" in data:
        account.last_name = data["surname"]
    return jsonify({"message": "Account updated"}), 200

@app.route("/api/accounts/<pesel>", methods=['DELETE'])
def delete_account(pesel):
    print("Delete account recieved")
    account = registry.find_account_by_pesel(pesel)
    if not account:
        return jsonify({"message": "Account not found"}), 404
    registry.delete_account_by_pesel(pesel)
    return jsonify({"message": "Account deleted"}), 200

@app.route("/api/accounts/<pesel>/transfer", methods=['POST'])
def transfer(pesel):
    data = request.get_json()
    print("Transfer for account recieved")
    print(f"Transfer for account request: {data}")
    account = registry.find_account_by_pesel(pesel)
    if not account:
        return jsonify({"message": "Account not found"}), 404


    if data["type"] == "incoming":
        account.transfer_in(data["amount"])
        return jsonify({"message": "The request has been accepted for processing"}), 200

    elif data["type"] == "outgoing":
        if account.balance<data["amount"]:
            return jsonify({"message": "Transfer did not go through - Not enough funds"}), 422
        account.transfer_out(data["amount"])
        return jsonify({"message": "The request has been accepted for processing"}), 200

    elif data["type"] == "express":
        if account.balance<data["amount"]:
            return jsonify({"message": "Transfer did not go through - Not enough funds"}), 422
        account.express_transfer_out(data["amount"])
        return jsonify({"message": "The request has been accepted for processing"}), 200

    else:
        return jsonify({"message": "Type does not exist"}), 422


