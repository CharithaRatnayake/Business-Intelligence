import flask

import database.configurations as db
import blockchain
from datetime import datetime
import model as model
import json

from blockchain.__init__ import Block, Blockchain as bc

app = flask.Flask(__name__)
db_cursor = db.db_cursor


@app.route('/getEssentials', methods=['POST'])
def getEssentials():
    rsp = getEssentials(flask.request.get_json())

    return json.dumps(rsp.__dict__)


@app.route('/register', methods=['POST'])
def register():
    msg_received = flask.request.get_json()
    msg_subject = msg_received["subject"]

    return register(msg_received)


@app.route('/login', methods=['POST'])
def login():
    msg_received = flask.request.get_json()
    msg_subject = msg_received["subject"]

    return login(msg_received)


@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = []
    for block in bc.chain:
        chain_data.append(block.__dict__)
    return json.dumps({"length": len(chain_data),
                       "chain": chain_data})


def register(msg_received):
    uid = msg_received["uid"]
    user_type = msg_received["user_type"]
    full_name = msg_received["full_name"]
    email = msg_received["email"]
    password = msg_received["password"]
    phone_number = msg_received["phone_number"]
    birth_day = msg_received["birth_day"]
    address = msg_received["address"]
    gender = msg_received["gender"]

    select_query = "SELECT * FROM users where email = " + "'" + email + "'"
    db_cursor.execute(select_query)
    records = db_cursor.fetchall()
    if len(records) != 0:
        return "Another user used the username. Please chose another username."

    insert_query = "INSERT INTO users (first_name, last_name, username, password) VALUES (%s, %s, %s, MD5(%s))"
    insert_query = "INSERT INTO `user` (`id`, `uid`, `user_type`, `full_name`, `email`, `password`, `phone_number`, " \
                   "`birth_day`, `address`, `gender`, `is_active`, `created_at`, `updated_at`) " \
                   "VALUES (NULL, MD5(%s), %s, %s, %s, MD5(password), %s, %s, %s, %s, '1', '" + datetime.now().timestamp() + "', '" + datetime.now().timestamp() + "'))"
    insert_values = (uid, user_type, full_name, email, password, phone_number, birth_day, address, gender)
    try:
        db_cursor.execute(insert_query, insert_values)
        db_cursor.commit()
        return "success"
    except Exception as e:
        print("Error while inserting the new record :", repr(e))
        return "failure"


def login(msg_received):
    email = msg_received["email"]
    password = msg_received["password"]

    select_query = "SELECT first_name, last_name FROM users where username = " + "'" + email + "' and password = " + "MD5('" + password + "')"
    db_cursor.execute(select_query)
    records = db_cursor.fetchall()

    if len(records) == 0:
        return "failure"
    else:
        return "success"


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
