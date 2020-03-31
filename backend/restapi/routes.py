import logging
import functools

from backend.restapi import restapi
from backend.restapi.database import Cursor
from flask import request, jsonify, abort

"""
<note>
NIGHTMARE NIGHTMARE NIGHTMARE NIGHTMARE!
Never in my life have I written anything more hacky, stupid and repetitive
than this file. This is why people use libraries and frameworks.
You've been warned.
</note>

This file defines all the REST endpoints for performing CRUD operations on 
the database.

the endpoints are either
table_name/new
table_name/get

endpoints that end with 'new' expect a POST request containing all the 
attribute/value pairs encoded as a JSON. 
endpoints that end with 'get' expect either a GET request with no parameters
(in that case they return all the tuples in the respective table)
or a POST request with one key/value pair.
(in that case they sort the result with a query of type SELECT * FROM TABLE_NAME WHERE
key=value;)
The only two special endpoints are
employee/login 
account/login
They differ from the rest in that they require a POST request containing both the username
and password (the names of the keys should be the same as respective column names in the table).
In case of success, they return an employee/account JSON, otherwise they return a 404 error.
"""
# TODO
#   change the error handling. Current way doesn't play nicely with psycopg
#   error messages (they contain %'s which are interpreted as string interpolation
#   by python's logging module.)

# Get module logger
logger = logging.getLogger(__name__)


# Now this is what I meant when I mentioned stupidity
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
        return None
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


@restapi.route("/branch/new", methods=["POST"])
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
        logger.error(e)
        abort(404)


@restapi.route("/branch/get", methods=["GET", "POST"])
def branch_get():
    try:
        req_json = request.json
        res = None
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
        logger.error(e)
        abort(404)


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


@restapi.route("/employee/new", methods=["POST"])
def employee_new():
    try:
        request_data = request.json
        with Cursor(commit=True) as cursor:
            cursor.execute("INSERT INTO employee (employee_username, employee_password,"
                           " branch, manager, salary, position) VALUES (%s, %s, %s, %s, %s, %s, %s)",
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
        logger.error(e)
        abort(404)


@restapi.route("/employee/login", methods=["POST"])
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
        logger.error(e)
        abort(404)


@restapi.route("/employee/get", methods=["GET", "POST"])
def employee_get():
    employee_convert_many = functools.partial(tuples_to_dicts, attrs=employee_attrs)
    try:
        req_json = request.json
        res = None
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
        logger.error(e)
        abort(404)


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


@restapi.route("/", methods=["GET"])
def test():
    try:
        return "Welcome"
    except:
        abort(500)

@restapi.route("/account/new", methods=["POST"])
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
        logger.error(e)
        abort(404)


@restapi.route("/account/login", methods=["POST"])
def account_login():
    account_convert_one = functools.partial(tuple_to_dict, attrs=account_attrs)
    try:
        request_data = request.json
        with Cursor(commit=False) as cursor:
            cursor.execute("SELECT * FROM Account WHERE username=%s AND account_password=%s", (
                request_data['username'],
                request_data['account_password']
            ))
            res = account_convert_one(tups=cursor.fetchone())
        return jsonify(res)
    except Exception as e:
        logger.error(e)
        abort(404)


@restapi.route("/account/get", methods=["GET", "POST"])
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
        logger.error(e)
        abort(404)


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


@restapi.route("/pricing/new", methods=["POST"])
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
        logger.error(e)
        abort(404)

#TODO: I STOPPED HERE

@restapi.route("/pricing/get", methods=["GET", "POST"])
def pricing_get():
    pass


# RentalProperty endpoints
# /rentalproperty/new
# /rentalproperty/get/property_id
# /rentalproperty/get/owner_id
# /rentalproperty/get/country
# /rentalproperty/get/all

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

rentalproperty_convert_one = functools.partial(tuple_to_dict, attrs=rentalproperty_attrs)
rentalproperty_convert_many = functools.partial(tuples_to_dicts, attrs=rentalproperty_attrs)


@restapi.route("/rentalproperty/new", methods=["POST"])
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
        logger.error(e)
        abort(404)


@restapi.route("/rentalproperty/get/property_id", methods=["POST"])
def rentalproperty_get_property_id():
    try:
        request_data = request.json
        with Cursor(commit=False) as cursor:
            cursor.execute("SELECT * FROM rentalproperty WHERE property_id=%s",
                           (
                               request_data["property_id"],
                           ))
            rp_tuple = cursor.fetchone()
        rp_dict = rentalproperty_convert_one(tup=rp_tuple)
        return jsonify(rp_dict)
    except Exception as e:
        logger.error(e)
        abort(404)


@restapi.route("/rentalproperty/get/owner_id", methods=["POST"])
def rentalproperty_get_owner_id():
    try:
        request_data = request.json
        with Cursor(commit=False) as cursor:
            cursor.execute("SELECT * FROM rentalproperty WHERE owner_id=%s",
                           (
                               request_data["owner_id"],
                           ))
            rp_tuples = cursor.fetchall()
        rp_dict = rentalproperty_convert_many(tups=rp_tuples)
        return jsonify(rp_dict)
    except Exception as e:
        logger.error(e)
        abort(404)


@restapi.route("/rentalproperty/get/country", methods=["POST"])
def rentalproperty_get_country():
    try:
        request_data = request.json
        with Cursor(commit=False) as cursor:
            cursor.execute("SELECT * FROM rentalproperty WHERE country=%s",
                           (request_data["country"],))
            rp_tuples = cursor.fetchall()
        rp_dict = rentalproperty_convert_many(tups=rp_tuples)
        return jsonify(rp_dict)
    except Exception as e:
        logger.error(e)
        abort(404)


@restapi.route("/rentalproperty/get/all", methods=["POST"])
def rentalproperty_get_all():
    try:
        with Cursor(commit=False) as cursor:
            cursor.execute("SELECT * FROM rentalproperty")
            rp_tuples = cursor.fetchall()
        res = rentalproperty_convert_many(tups=rp_tuples)
        return jsonify(res)
    except Exception as e:
        logger.error(e)
        abort(404)


# RentalAgreement endpoints
# /rentalagreement/new
# /rentalagreement/get/all
# /rentalagreement/get/agreement_id
# /rentalagreement/get/host_id
# /rentalagreement/get/guest_id

rentalagreement_attrs = [
    "agreement_id",
    "host_id",
    "guest_id",
    "property_id",
    "signing_date",
    "total_amount"
]

rentalagreement_convert_one = functools.partial(tuple_to_dict, attrs=rentalagreement_attrs)
rentalagreement_convert_many = functools.partial(tuples_to_dicts, attrs=rentalagreement_attrs)


@restapi.route("/rentalagreement/new", methods=["POST"])
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
        logger.error(e)
        abort(404)


@restapi.route("/rentalagreement/get/all", methods=["POST"])
def rentalagreement_get_all():
    try:
        with Cursor(commit=False) as cursor:
            cursor.execute("SELECT * FROM rentalagreement")
            ra_tuples = cursor.fetchall()
        res = rentalagreement_convert_many(tups=ra_tuples)
        return jsonify(res)
    except Exception as e:
        logger.error(e)
        abort(404)


@restapi.route("/rentalagreement/get/agreement_id", methods=["POST"])
def rentalagreement_get_agreement_id():
    try:
        request_data = request.json
        with Cursor(commit=False) as cursor:
            cursor.execute("SELECT * FROM rentalagreement where agreement_id=%s",
                           (
                               request_data["agreement_id"],
                           ))
            ra_tuple = cursor.fetchone()
        res = rentalagreement_convert_one(tup=ra_tuple)
        return jsonify(res)
    except Exception as e:
        logger.error(e)
        abort(404)


@restapi.route("/rentalagreement/get/host_id", methods=["POST"])
def rentalagreement_get_host_id():
    try:
        request_data = request.json
        with Cursor(commit=False) as cursor:
            cursor.execute("SELECT * FROM rentalagreement WHERE host_id=%s",
                           (
                               request_data["host_id"],
                           ))
            ra_tuple = cursor.fetchall()
        res = rentalagreement_convert_many(tups=ra_tuple)
        return jsonify(res)
    except Exception as e:
        logger.error(e)
        abort(404)
