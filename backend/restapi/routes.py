import functools

from flask import request, jsonify, abort

from backend.restapi import app
from backend.restapi.database import Cursor

"""
<note>
NIGHTMARE NIGHTMARE NIGHTMARE NIGHTMARE!
A LOT OF SPAGETTI CODE BELOW. YOU'VE BEEN WARNED.
</note>

This file defines all the REST endpoints for performing CRUD operations on 
the database.

the endpoints are either
table_name/new
table_name/get

endpoints that end with 'new' expect a POST request containing all the 
attribute/value pairs encoded in JSON. 
endpoints that end with 'get' expect either a GET request with no parameters
(in that case they return all the tuples in their respective table)
or a POST request with one key/value pair
(in that case they sort the result with a query of type SELECT * FROM TABLE_NAME WHERE
key=value;)
The only two special endpoints are
employee/login 
account/login
They differ from the rest in that they require a POST request containing both the username
and password (the names of the keys should be the same as respective column names in the table).
In case of success, they return an employee/account JSON, otherwise they return a 404 error.
"""


def tuple_to_dict(attrs, tup):
    """
    Function to convert a tuple from the database
    to a dictionary of the form {"attribute_name": value}.
    Args:
        attrs (list[str]): attributes of the table IN THE ORDER THAT THEY APPEAR IN THE DATABASE.
        tup (tuple[object]): database tuple.

    Returns:
        dict: resulting dictionary
    """
    res = {}
    for i in range(len(attrs)):
        res[attrs[i]] = tup[i]
    return res


def tuples_to_dicts(attrs, tups):
    """
    Function to convert a list of tuples from the database
    to a list of dicts.
    Args:
        attrs (list[str]): attributes of the table IN THE ORDER THAT THEY APPEAR IN THE DATABASE.
        tups (list[tuple]): list of tuples retrieved from db
    Returns:
        list[dict]: list of resulting dictionaries
    """
    if not tups:
        return []
    dicts = []
    part = functools.partial(tuple_to_dict, attrs=attrs)
    for t in tups:
        dicts.append(part(tup=t))
    return dicts


# Branch endpoints:
# /branch/new
# /branch/get

branch_attrs = [
    "country",
    "branch_manager"
]

branch_convert_many = functools.partial(tuples_to_dicts, attrs=branch_attrs)


@app.route("/branch/new", methods=["POST"])
def branch_new():
    try:
        request_data = request.json
        with Cursor(commit=True) as cursor:
            cursor.execute("INSERT INTO branch (country, branch_manager) VALUES (%s, %s)",
                           (
                               request_data["country"],
                               request_data["branch_manager"]
                           ))
            return 'OK', 200
    except Exception as e:
        app.logger.error(e)
        abort(400)


@app.route("/branch/get", methods=["GET", "POST"])
def branch_get():
    try:
        req_json = request.json
        with Cursor(commit=False) as cur:
            if request.method == "GET":
                cur.execute("SELECT * FROM branch")
            else:
                if "country" in req_json:
                    cur.execute("SELECT * FROM branch WHERE country=%s", (req_json["country"],))
                elif "branch_manager" in req_json:
                    cur.execute("SELECT * FROM branch WHERE branch_manager=%s", (req_json["branch_manager"],))
            res = branch_convert_many(tups=cur.fetchall())
        return jsonify(res)
    except Exception as e:
        app.logger.error(e)
        abort(400)


# Employee endpoints:
# /employee/new
# /employee/login
# /employee/get

employee_attrs = [
    "employee_id",
    "employee_username",
    "employee_password",
    "branch",
    "manager",
    "salary",
    "position"
]


@app.route("/employee/new", methods=["POST"])
def employee_new():
    try:
        request_data = request.json
        with Cursor(commit=True) as cursor:
            cursor.execute("INSERT INTO employee (employee_username, employee_password,"
                           " branch, manager, salary, position) VALUES (%s, %s, %s, %s, %s, %s)",
                           (
                               request_data["employee_username"],
                               request_data["empoyee_password"],
                               request_data["branch"],
                               request_data["manager"],
                               request_data["salary"],
                               request_data["position"]
                           ))
        return 'OK', 200
    except Exception as e:
        app.logger.error(e)
        abort(400)


@app.route("/employee/login", methods=["POST"])
def employee_login():
    employee_convert_one = functools.partial(tuple_to_dict, attrs=employee_attrs)
    try:
        request_data = request.json
        with Cursor(commit=False) as cursor:
            cursor.execute("SELECT * FROM employee WHERE employee_username=%s AND employee_password=%s",
                           (
                               request_data["employee_username"],
                               request_data["employee_password"]
                           ))
            res = employee_convert_one(tups=cursor.fetchone())
        return jsonify(res)
    except Exception as e:
        app.logger.error(e)
        abort(400)


@app.route("/employee/get", methods=["GET", "POST"])
def employee_get():
    employee_convert_many = functools.partial(tuples_to_dicts, attrs=employee_attrs)
    try:
        req_json = request.json
        with Cursor(commit=False) as cur:
            if request.method == "GET":
                cur.execute("SELECT * FROM employee")
            else:
                if "employee_id" in req_json:
                    cur.execute("SELECT * FROM employee WHERE employee_id=%s", (req_json["employee_id"],))
                elif "branch" in req_json:
                    cur.execute("SELECT * FROM employee WHERE branch=%s", (req_json["branch"],))
                elif "manager" in req_json:
                    cur.execute("SELECT * FROM employee WHERE manager=%s", (req_json["manager"],))
                elif "salary" in req_json:
                    cur.execute("SELECT * FROM employee WHERE salary=%s", (req_json["salary"],))
                elif "position" in req_json:
                    cur.execute("SELECT * FROM employee WHERE position=%s", (req_json["position"],))
            res = employee_convert_many(tups=cur.fetchall())
        return jsonify(res)
    except Exception as e:
        app.logger.error(e)
        abort(400)


# Account endpoints:
# /account/new
# /account/login
# /account/get

account_attrs = [
    "account_id",
    "first_name",
    "last_name",
    "email",
    "phone",
    "username",
    "account_password"
]


@app.route("/", methods=["GET"])
def test():
    return "Welcome"


@app.route("/account/new", methods=["POST"])
def account_new():
    try:
        request_data = request.json
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
        return 'OK', 200
    except Exception as e:
        app.logger.error(e)
        abort(400)


@app.route("/account/login", methods=["POST"])
def account_login():
    account_convert_one = functools.partial(tuple_to_dict, attrs=account_attrs)
    try:
        request_data = request.json
        with Cursor(commit=False) as cursor:
            cursor.execute("SELECT * FROM Account WHERE username=%s AND account_password=%s", (
                request_data['username'],
                request_data['account_password']
            ))
            res = account_convert_one(tup=cursor.fetchone())
        return jsonify(res)
    except Exception as e:
        app.logger.error(e)
        abort(400)


@app.route("/account/get", methods=["GET", "POST"])
def account_get():
    account_convert_many = functools.partial(tuples_to_dicts, attrs=account_attrs)
    try:
        req_json = request.json
        with Cursor(commit=False) as cursor:
            if request.method == "GET":
                cursor.execute("SELECT * FROM account")
            else:
                if "account_id" in req_json:
                    cursor.execute("SELECT * FROM account WHERE account_id=%s", (req_json["account_id"],))
                elif "first_name" in req_json:
                    cursor.execute("SELECT * FROM account WHERE first_name=%s", (req_json["first_name"],))
                elif "last_name" in req_json:
                    cursor.execute("SELECT * FROM account WHERE last_name=%s", (req_json["last_name"],))
                elif "email" in req_json:
                    cursor.execute("SELECT * FROM account WHERE email=%s", (req_json["email"],))
                elif "phone" in req_json:
                    cursor.execute("SELECT * FROM account WHERE phone=%s", (req_json["phone"],))
            res = account_convert_many(tups=cursor.fetchall())
        return jsonify(res)
    except Exception as e:
        app.logger.error(e)
        abort(400)


# Pricing endpoints
# /pricing/new
# /pricing/get

pricing_attrs = [
    "pricing_id",
    "class_name",
    "host",
    "price",
    "home_type",
    "rules",
    "amenities",
    "accomodates"
]


@app.route("/pricing/new", methods=["POST"])
def pricing_new():
    try:
        request_data = request.json
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
            return 'OK', 200
    except Exception as e:
        app.logger.error(e)
        abort(400)


@app.route("/pricing/get", methods=["GET", "POST"])
def pricing_get():
    pricing_convert_many = functools.partial(tuples_to_dicts, attrs=pricing_attrs)
    try:
        req_json = request.json
        with Cursor(commit=False) as cursor:
            if request.method == "GET":
                cursor.execute("SELECT * FROM pricing")
            else:
                if "pricing_id" in req_json:
                    cursor.execute("SELECT * FROM pricing WHERE pricing_id=%s", (req_json["pricing_id"],))
                elif "class_name" in req_json:
                    cursor.execute("SELECT * FROM pricing WHERE class_name=%s", (req_json["class_name"],))
                elif "host" in req_json:
                    cursor.execute("SELECT * FROM pricing WHERE host=%s", (req_json["host"],))
                elif "price" in req_json:
                    cursor.execute("SELECT * FROM pricing WHERE price=%s", (req_json["price"],))
                elif "home_type" in req_json:
                    cursor.execute("SELECT * FROM pricing WHERE home_type=%s", (req_json["home_type"],))
                elif "rules" in req_json:
                    cursor.execute("SELECT * FROM pricing WHERE rules=%s", (req_json["rules"],))
                elif "amenities" in req_json:
                    cursor.execute("SELECT * FROM pricing WHERE amenities=%s", (req_json["amenities"],))
                elif "accomodates" in req_json:
                    cursor.execute("SELECT * FROM pricing WHERE accomodates=%s", (req_json["accomodates"],))
            res = pricing_convert_many(tups=cursor.fetchall())
        return jsonify(res)
    except Exception as e:
        app.logger.error(e)
        abort(400)


# RentalProperty endpoints
# /rentalproperty/new
# /rentalproperty/get

rentalproperty_attrs = [
    "property_id",
    "city",
    "street",
    "street_no",
    "unit",
    "zip",
    "state_province",
    "country",
    "owner_id",
    "property_type",
    "room_type",
    "pricing_id",
    "bathroom",
    "bedroom",
    "bed"
]


@app.route("/rentalproperty/new", methods=["POST"])
def rentalproperty_new():
    try:
        request_data = request.json
        with Cursor(commit=True) as cursor:
            cursor.execute("INSERT INTO rentalproperty (city, street, street_no, unit, zip,"
                           " state_province, country, owner_id, property_type, room_type,"
                           " pricing_id, bathroom, bedroom, bed) VALUES "
                           "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (
                               request_data["city"],
                               request_data["street"],
                               request_data["street_no"],
                               request_data["unit"],
                               request_data["zip"],
                               request_data["state_provice"],
                               request_data["country"],
                               request_data["owner_id"],
                               request_data["property_type"],
                               request_data["room_type"],
                               request_data["pricing_id"],
                               request_data["bathroom"],
                               request_data["bedroom"],
                               request_data["bed"]
                           ))
        return 'OK', 200
    except Exception as e:
        app.logger.error(e)
        abort(400)


# NOW THIS IS SOME GREAT FUCKING SPAGHETTI
@app.route("/rentalproperty/get", methods=["GET", "POST"])
def rentalproperty_get():
    rentalproperty_convert_many = functools.partial(tuples_to_dicts, attrs=rentalproperty_attrs)
    try:
        req_json = request.json
        with Cursor(commit=False) as cur:
            if request.method == "GET":
                cur.execute("SELECT * FROM rentalproperty")
            else:
                if "city" in req_json:
                    cur.execute("SELECT * FROM rentalproperty WHERE city=%s", (req_json["city"],))
                elif "street" in req_json:
                    cur.execute("SELECT * FROM rentalproperty WHERE street=%s", (req_json["street"],))
                elif "street_no" in req_json:
                    cur.execute("SELECT * FROM rentalproperty WHERE street_no=%s", (req_json["street_no"],))
                elif "unit" in req_json:
                    cur.execute("SELECT * FROM rentalproperty WHERE unit=%s", (req_json["unit"],))
                elif "zip" in req_json:
                    cur.execute("SELECT * FROM rentalproperty WHERE zip=%s", (req_json["zip"],))
                elif "state_province" in req_json:
                    cur.execute("SELECT * FROM rentalproperty WHERE state_province=%s", (req_json["state_province"],))
                elif "country" in req_json:
                    cur.execute("SELECT * FROM rentalproperty WHERE country=%s", (req_json["country"],))
                elif "owner_id" in req_json:
                    cur.execute("SELECT * FROM rentalproperty WHERE owner_id=%s", (req_json["owner_id"],))
                elif "property_type" in req_json:
                    cur.execute("SELECT * FROM rentalproperty WHERE property_type=%s", (req_json["property_type"],))
                elif "room_type" in req_json:
                    cur.execute("SELECT * FROM rentalproperty WHERE room_type=%s", (req_json["room_type"],))
                elif "pricing_id" in req_json:
                    cur.execute("SELECT * FROM rentalproperty WHERE pricing_id=%s", (req_json["pricing_id"],))
                elif "bathroom" in req_json:
                    cur.execute("SELECT * FROM rentalproperty WHERE bathroom=%s", (req_json["bathroom"],))
                elif "bedroom" in req_json:
                    cur.execute("SELECT * FROM rentalproperty WHERE bedroom=%s", (req_json["bedroom"],))
                elif "bed" in req_json:
                    cur.execute("SELECT * FROM rentalproperty WHERE bed=%s", (req_json["bed"],))
            res = rentalproperty_convert_many(tups=cur.fetchall())
        return jsonify(res)
    except Exception as e:
        app.logger.error(e)
        abort(400)


# RentalAgreement endpoints
# /rentalagreement/new
# /rentalagreement/get

rentalagreement_attrs = [
    "agreement_id",
    "host_id",
    "guest_id",
    "property_id",
    "signing_date",
    "total_amount"
]


@app.route("/rentalagreement/new", methods=["POST"])
def rentalagreement_new():
    try:
        request_data = request.json
        with Cursor(commit=True) as cursor:
            cursor.execute("INSERT INTO rentalagreement (host_id, guest_id, property_id,"
                           " signing_date, total_amount) VALUES (%s, %s, %s, %s, %s)",
                           (
                               request_data["host_id"],
                               request_data["guest_id"],
                               request_data["property_id"],
                               request_data["signing_date"],
                               request_data["total_amount"]
                           ))
        return 'OK', 200
    except Exception as e:
        app.logger.error(e)
        abort(400)


@app.route("/rentalagreement/get", methods=["GET", "POST"])
def rentalagreement_get():
    rentalagreement_convert_many = functools.partial(tuples_to_dicts, attrs=rentalagreement_attrs)
    try:
        req_json = request.json
        with Cursor(commit=False) as cur:
            if request.method == "GET":
                cur.execute("SELECT * FROM rentalagreement")
            else:
                if "agreement_id" in req_json:
                    cur.execute("SELECT * FROM rentalagreement WHERE agreement_id=%s", (req_json["agreement_id"],))
                elif "host_id" in req_json:
                    cur.execute("SELECT * FROM rentalagreement WHERE host_id=%s", (req_json["host_id"],))
                elif "guest_id" in req_json:
                    cur.execute("SELECT * FROM rentalagreement WHERE guest_id=%s", (req_json["guest_id"],))
                elif "property_id" in req_json:
                    cur.execute("SELECT * FROM rentalagreement WHERE property_id=%s", (req_json["property_id"],))
                elif "signing_date" in req_json:
                    cur.execute("SELECT * FROM rentalagreement WHERE signing_date=%s", (req_json["signing_date"],))
                elif "total_amount" in req_json:
                    cur.execute("SELECT * FROM rentalagreement WHERE total_amount=%s", (req_json["total_amount"],))
            res = rentalagreement_convert_many(tups=cur.fetchall())
        return jsonify(res)
    except Exception as e:
        app.logger.error(e)
        abort(400)


# RentalDate endpoints
# /rentaldate/new
# /rentaldate/get

rentaldate_attrs = [
    "rental_date",
    "property_id",
    "agreement_id"
]


@app.route("/rentaldate/new", methods=["POST"])
def rentaldate_new():
    try:
        req_json = request.json
        with Cursor(commit=True) as cur:
            cur.execute("INSERT INTO rentaldate (rental_date, property_id, agreement_id) VALUES (%s, %s, %s)",
                        (
                            req_json["rental_date"],
                            req_json["property_id"],
                            req_json["agreement_id"]
                        ))
        return 'OK', 200
    except Exception as e:
        app.logger.error(e)
        abort(400)


@app.route("/rentaldate/get", methods=["GET", "POST"])
def rentaldate_get():
    rentaldate_convert_many = functools.partial(tuples_to_dicts, attrs=rentaldate_attrs)
    try:
        req_json = request.json
        with Cursor(commit=False) as cur:
            if request.method == "GET":
                cur.execute("SELECT * FROM rentaldate")
            else:
                if "rental_date" in req_json:
                    cur.execute("SELECT * FROM rentaldate WHERE rental_date=%s", (req_json["rental_date"],))
                elif "property_id" in req_json:
                    cur.execute("SELECT * FROM rentaldate WHERE property_id=%s", (req_json["property_id"],))
                elif "agreement_id" in req_json:
                    cur.execute("SELECT * FROM rentaldate WHERE agreement_id=%s", (req_json["agreement_id"]))
            res = rentaldate_convert_many(tups=cur.fetchall())
        return jsonify(res)
    except Exception as e:
        app.logger.error(e)
        abort(400)


# Review endpoints
# /review/new
# /review/get

review_attrs = [
    "review_id",
    "reviewer",
    "property",
    "comment",
    "stars",
    "cleanliness",
    "communications",
    "overall_value"
]


@app.route("/review/new", methods=["POST"])
def review_new():
    try:
        req_json = request.json
        with Cursor(commit=True) as cur:
            cur.execute("INSERT INTO review (reviewer, property, comment, stars,"
                        " cleanliness, communications, overall_value) VALUES ("
                        "%s, %s, %s, %s, %s, %s, %s)", (
                            req_json["reviewer"],
                            req_json["property"],
                            req_json["comment"],
                            req_json["stars"],
                            req_json["cleanliness"],
                            req_json["communications"],
                            req_json["overall_value"]
                        ))
        return 'OK', 200
    except Exception as e:
        app.logger.error(e)
        abort(400)


@app.route("/review/get", methods=["GET", "POST"])
def review_get():
    review_convert_many = functools.partial(tuples_to_dicts, attrs=review_attrs)
    try:
        req_json = request.json
        with Cursor(commit=False) as cur:
            if request.method == "GET":
                cur.execute("SELECT * FROM review")
            else:
                if "reviewer" in req_json:
                    cur.execute("SELECT * FROM review WHERE reviewer=%s", (req_json["reviewer"],))
                elif "property" in req_json:
                    cur.execute("SELECT * FROM review WHERE property=%s", (req_json["property"],))
                elif "comment" in req_json:
                    cur.execute("SELECT * FROM review WHERE comment=%s", (req_json["comment"],))
                elif "stars" in req_json:
                    cur.execute("SELECT * FROM review WHERE stars=%s", (req_json["stars"],))
                elif "cleanliness" in req_json:
                    cur.execute("SELECT * FROM review WHERE cleanliness=%s", (req_json["cleanliness"],))
                elif "communications" in req_json:
                    cur.execute("SELECT * FROM review WHERE communications=%s", (req_json["communications"],))
                elif "overall_value" in req_json:
                    cur.execute("SELECT * FROM review WHERE overall_value=%s", (req_json["overall_value"],))
            res = review_convert_many(tups=cur.fetchall())
        return jsonify(res)
    except Exception as e:
        app.logger.error(e)
        abort(400)


# Payment endpoints
# /payment/new
# /payment/get

payment_attrs = [
    "transaction_id",
    "paid_by",
    "paid_to",
    "agreement_id",
    "payment_type",
    "is_complete",
    "amount"
]


@app.route("/payment/new", methods=["POST"])
def payment_new():
    try:
        req_json = request.json
        with Cursor(commit=True) as cur:
            cur.execute(
                "INSERT INTO payment (paid_by, paid_to, agreement_id, payment_type, is_complete, amount) VALUES "
                "(%s, %s, %s, %s, %s, %s)", (
                    req_json["paid_by"],
                    req_json["paid_to"],
                    req_json["agreement_id"],
                    req_json["payment_type"],
                    req_json["is_complete"],
                    req_json["amount"]
                ))
        return 'OK', 200
    except Exception as e:
        app.loger.error(e)
        abort(400)


@app.route("/payment/get", methods=["GET", "POST"])
def payment_get():
    payment_convert_many = functools.partial(tuples_to_dicts, attrs=payment_attrs)
    try:
        req_json = request.json
        with Cursor(commit=False) as cur:
            if request.method == "GET":
                cur.execute("SELECT * FROM payment")
            else:
                if "paid_by" in req_json:
                    cur.execute("SELECT * FROM payment WHERE paid_by=%s", (req_json["paid_by"],))
                elif "paid_to" in req_json:
                    cur.execute("SELECT * FROM payment WHERE paid_to=%s", (req_json["paid_to"],))
                elif "agreement_id" in req_json:
                    cur.execute("SELECT * FROM payment WHERE agreement_id=%s", (req_json["agreement_id"],))
                elif "payment_type" in req_json:
                    cur.execute("SELECT * FROM payment WHERE payment_type=%s", (req_json["payment_type"],))
                elif "is_complete" in req_json:
                    cur.execute("SELECT * FROM payment WHERE is_complete=%s", (req_json["is_complete"],))
                elif "amount" in req_json:
                    cur.execute("SELECT * FROM payment WHERE amount=%s", (req_json["amount"],))
            res = payment_convert_many(tups=cur.fetchall())
        return jsonify(res)
    except Exception as e:
        app.logger.error(e)
        abort(400)
