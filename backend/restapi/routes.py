from backend.restapi import restapi
from backend.restapi.database import Cursor
from flask import request, jsonify, abort


@restapi.route("/", methods=["GET"])
def test():
    try:
        return "Welcome"
    except:
        abort(500)

@restapi.route("/account/new", methods=["POST"])
def new_account():
    request_data = request.json
    try:
        with Cursor(commit=True) as cursor:
            cursor.execute("INSERT INTO Account "
                           "(first_name, last_name, email, phone, username, account_password) "
                           "VALUES (%s, %s, %s, %s, %s, %s)", (
                               request_data['first_name'],
                               request_data['last_name'],
                               request_data['email'],
                               request_data['phone'],
                               request_data['username'],
                               request_data['account_password']
                           ))
        return 'OK'
    except:
        abort(404)


@restapi.route("/account/get", methods=["POST"])
def get_account():
    request_data = request.json
    try:
        with Cursor(commit=False) as cursor:
            cursor.execute("SELECT * FROM Account WHERE username=%s AND account_password=%s", (
                request_data['username'],
                request_data['account_password']
            ))
            account_tuple = cursor.fetchone()
            print(account_tuple)
        account_dict = {
            "account_id": account_tuple[0],
            "first_name": account_tuple[1],
            "last_name": account_tuple[2],
            "email": account_tuple[3],
            "phone": account_tuple[4]
        }
        return jsonify(account_dict)
    except:
        abort(404)


@restapi.route("pricing/new", methods=["POST"])
def new_pricing():
    request_data = request.json
    try:
        with Cursor(commit=True) as cursor:
            cursor.execute("INSERT INTO Pricing "
                           "(class_name, host, price, home_type, rules, amenities, accomodates) VALUES "
                           "(%s, %s, %s, %s, %s, %s, %s)", (
                               request_data["class_name"],
                               request_data["host"],
                               request_data["price"],
                               request_data["home_type"],
                               request_data["rules"],
                               request_data["amenities"],
                               request_data["accomodates"]
                           ))
            return 'OK'
    except:
        abort(404)


@restapi.route("pricing/get", methods=["POST"])
def get_pricing():
    request_data = request.json
    try:
        with Cursor(commit=False) as cursor:
            cursor.execute("SELECT * FROM Pricing WHERE host=%s", (request_data["host"],))
            res = cursor.fetchall()
            return jsonify(res)
    except:
        abort(404)
