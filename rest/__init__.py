import flask

import database.configurations as db
import blockchain
from datetime import datetime
import model as model
import json
import rest.response
from rest.response import Response
import hashlib

from blockchain.__init__ import Block, Blockchain as bc

app = flask.Flask(__name__)
db_cursor = db.db_cursor
connection = db


@app.route('/getEssentials', methods=['POST'])
def getEssentials():
    rsp = getEssentials(flask.request.get_json())

    return json.dumps(rsp.__dict__)


@app.route('/register', methods=['POST'])
def register():
    msg_received = flask.request.get_json()
    rsp = register(msg_received)
    return json.dumps(rsp.__dict__)


@app.route('/login', methods=['POST'])
def login():
    msg_received = flask.request.get_json()
    rsp = login(msg_received)
    return json.dumps(rsp.__dict__)


@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = []
    for block in bc.chain:
        chain_data.append(block.__dict__)
    return json.dumps({"length": len(chain_data),
                       "chain": chain_data})


def register(msg_received):
    user_type = msg_received["user_type"]
    full_name = msg_received["full_name"]
    email = msg_received["email"]
    password = msg_received["password"]
    phone_number = msg_received["phone_number"]
    birth_day = msg_received["birth_day"]
    address = msg_received["address"]
    gender = msg_received["gender"]
    is_active = 1
    created_at = 1
    updated_at = 1

    data_user = (email, user_type, full_name, email, password, phone_number, birth_day, address, gender, is_active,
                 created_at, updated_at)

    select_query = "SELECT * FROM user where email = " + "'" + email + "'"
    db_cursor.execute(select_query)
    records = db_cursor.fetchall()
    if len(records) != 0:
        p1 = Response(1, "Your email is already registered with the system.", None)
        return p1

    insert_query = '''INSERT INTO `user` (`id`, `uid`, `user_type`, `full_name`, `email`, `password`, `phone_number`, 
                    `birth_day`, `address`, `gender`, `is_active`, `created_at`, `updated_at`) 
                   VALUES (NULL, MD5(%s), %s, %s, %s, MD5(%s), %s, %s, %s, %s, %s, %s, %s)'''

    print(insert_query)
    print(data_user)

    try:
        db_cursor.execute(insert_query, data_user)
        connection.db.commit()

        select_query = "SELECT * FROM user where email = " + "'" + email + "' and password = " + "MD5('" + password + "')"
        db_cursor.execute(select_query)
        row_headers = [x[0] for x in db_cursor.description]
        records = db_cursor.fetchall()
        json_data = []
        for result in records:
            json_data.append(dict(zip(row_headers, result)))

        p1 = Response(0, "Success.", json_data[0])
        return p1
    except Exception as e:
        print("Error while inserting the new record :", repr(e))
        p1 = Response(1, "Your email or phone number is already registered with the system.", None)
        return p1


def login(msg_received):
    email = msg_received["email"]
    password = msg_received["password"]

    select_query = "SELECT * FROM user where email = " + "'" + email + "' and password = " + "MD5('" + password + "')"
    db_cursor.execute(select_query)
    row_headers = [x[0] for x in db_cursor.description]
    records = db_cursor.fetchall()
    json_data = []
    for result in records:
        json_data.append(dict(zip(row_headers, result)))

    if len(records) == 0:
        p1 = Response(1, "User not found.", None)
        return p1
    else:
        p1 = Response(0, "Success", json_data[0])
        return p1


def getEssentials(msg_received):
    print(msg_received)
    path = msg_received["path"]
    type = path.split("_", 2)
    category = msg_received["category"]
    sub_category = msg_received["sub_category"]

    print("Path name: " + path)
    print("Path Type: " + type[0])
    print("category: " + category)
    print("sub_category: " + sub_category)

    if type[0] == "price":
        model.model_price.runArima(type[1])
    elif type[0] == "quantity":
        model.model_quantity.runArima(type[1])
    elif type[0] == "sales":
        model.model_sales.runArima(type[1])
    elif type[0] == "import":
        return model.model_imports.runArima(type[1], category, sub_category)
    else:
        model.model_price.runArima(type[1])

    if len(0) == 0:
        return "failure"
    else:
        return "success"


app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)
