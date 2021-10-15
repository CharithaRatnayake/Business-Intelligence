import time
import flask
from flask import send_from_directory
import json
import rest.response
import os
from rest.response import Response
from apscheduler.schedulers.background import BackgroundScheduler

import database.configurations as db
from blockchain import Block, Blockchain
import model as model
import firebase as firebase

app = flask.Flask(__name__)
db_cursor = db.db_cursor
connection = db
blockchain = Blockchain()

UPLOAD_FOLDER = './upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def print_date_time():
    firebase.runPrediction()


scheduler = BackgroundScheduler()
scheduler.add_job(func=print_date_time, trigger="interval", seconds=60*60)
scheduler.start()


@app.route('/img/<filename>')
def send_file(filename):
    return send_from_directory("../upload", filename)


@app.route('/getEssentials', methods=['POST'])
def getEssentials():
    rsp = getEssentials(flask.request.get_json())

    return json.dumps(rsp.__dict__)


@app.route('/getCategories', methods=['GET'])
def getCategories():
    rsp = getCategories()

    return json.dumps(rsp.__dict__)


@app.route('/register', methods=['POST'])
def register():
    msg_received = flask.request.get_json()
    rsp = register(msg_received)
    return json.dumps(rsp.__dict__)


@app.route('/addOrganization', methods=['POST'])
def addOrganization():
    if 'logo' not in flask.request.files:
        return json.dumps(Response(1, "File not found.", None).__dict__)
    msg_received = flask.request.form
    user_id = msg_received["user_id"]
    file = flask.request.files['logo']
    path = os.path.join(app.config['UPLOAD_FOLDER'], user_id + "_org_" + file.filename)
    file.save(path)
    rsp = addOrganization(msg_received, user_id + "_org_" + file.filename)
    return json.dumps(rsp.__dict__)


@app.route('/getOrganization', methods=['GET'])
def getOrganization():
    rsp = getOrganization(flask.request.args)

    return json.dumps(rsp.__dict__)


@app.route('/addShop', methods=['POST'])
def addShop():
    rsp = addShop(flask.request.get_json())
    return json.dumps(rsp.__dict__)


@app.route('/getShops', methods=['GET'])
def getShops():
    rsp = getShops(flask.request.args)

    return json.dumps(rsp.__dict__)


@app.route('/getAllShops', methods=['GET'])
def getAllShops():
    rsp = getAllShops()

    return json.dumps(rsp.__dict__)


@app.route('/login', methods=['POST'])
def login():
    msg_received = flask.request.get_json()
    rsp = login(msg_received)
    return json.dumps(rsp.__dict__)


@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    return json.dumps({"length": len(chain_data),
                       "chain": chain_data})


@app.route('/complaints', methods=['POST'])
def complaints():
    msg_received = flask.request.get_json()
    rsp = complaints(msg_received)
    return json.dumps(rsp.__dict__)


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
            print(json_data)

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


def getCategories():
    select_query = "SELECT * FROM shop_type"
    db_cursor.execute(select_query)
    row_headers = [x[0] for x in db_cursor.description]
    records = db_cursor.fetchall()
    json_data = []
    for result in records:
        json_data.append(dict(zip(row_headers, result)))

    if len(records) == 0:
        p1 = Response(1, "Categories table seems to be empty.", None)
        return p1
    else:
        p1 = Response(0, "Success", json_data)
        return p1


def getOrganization(msg_received):
    user_id = msg_received["user_id"]
    select_query = '''SELECT * FROM organization where user_id = %s''' % user_id
    db_cursor.execute(select_query)
    row_headers = [x[0] for x in db_cursor.description]
    records = db_cursor.fetchall()
    json_data = []

    if len(records) == 0:
        p1 = Response(1, "No Organization found.", None)
        return p1

    for result in records:
        json_data.append(dict(zip(row_headers, result)))
        print(json_data)

    return Response(0, "Success.", json_data[0])


def addOrganization(msg_received, file):
    print(msg_received)
    name = msg_received["name"]
    logo = file
    description = msg_received["description"]
    category_id = 0
    shop_type_id = msg_received["shop_type_id"]
    user_id = msg_received["user_id"]
    is_active = 1
    created_at = 1
    updated_at = 1

    insert_query = '''INSERT INTO `organization` (`id`, `name`, `logo`, `description`, `is_active`, `created_at`, 
                    `updated_at`, `user_id`, `category_id`, `shop_type_id`) 
                   VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
    org = (name, logo, description, is_active, created_at, updated_at, user_id, category_id, shop_type_id)

    print(insert_query)
    print(org)

    try:
        db_cursor.execute(insert_query, org)
        connection.db.commit()

        select_query = "SELECT * FROM organization where user_id = " + "'" + user_id + "'"
        db_cursor.execute(select_query)
        row_headers = [x[0] for x in db_cursor.description]
        records = db_cursor.fetchall()
        json_data = []
        for result in records:
            json_data.append(dict(zip(row_headers, result)))

        return Response(0, "Success.", json_data[0])
    except Exception as e:
        print("Error while inserting the new record :", repr(e))
        p1 = Response(1, "We can't add your organization to the system.", None)
        return p1


def addShop(msg_received):
    print(msg_received)
    name = msg_received["name"]
    address = msg_received["address"]
    phonenumber = msg_received["phonenumber"]
    organization_id = msg_received["organization_id"]
    location = msg_received["location"]
    is_active = 1
    created_at = 1
    updated_at = 1

    insert_query = '''INSERT INTO `shop` (`id`, `name`, `address`, `phonenumber`, `organization_id`, `location`, 
                    `is_active`, `created_at`, `updated_at`) 
                   VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s)'''
    org = (name, address, phonenumber, organization_id, location, is_active, created_at, updated_at)

    print(insert_query)
    print(org)

    try:
        db_cursor.execute(insert_query, org)
        connection.db.commit()

        select_query = '''SELECT * FROM shop where organization_id = %s''' % organization_id
        db_cursor.execute(select_query)
        row_headers = [x[0] for x in db_cursor.description]
        records = db_cursor.fetchall()
        json_data = []
        for result in records:
            json_data.append(dict(zip(row_headers, result)))

        return Response(0, "Success.", json_data)
    except Exception as e:
        print("Error while inserting the new record :", repr(e))
        p1 = Response(1, "We can't add your shop to the system.", None)
        return p1


def complaints(msg_received):
    print(msg_received)
    uid = msg_received["uid"]
    name = msg_received["name"]
    email = msg_received["email"]
    title = msg_received["title"]
    description = msg_received["description"]
    url = ""
    is_active = 1
    created_at = 1
    updated_at = 1

    insert_query = '''INSERT INTO `report` (`id`, `uid`,`name`, `email`, `title`, `description`, `url`, 
                    `is_active`, `created_at`, `updated_at`) 
                   VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
    report = (uid, name, email, title, description, url, is_active, created_at, updated_at)

    print(insert_query)
    print(report)

    try:
        db_cursor.execute(insert_query, report)
        connection.db.commit()

        return Response(0, "Success.", None)
    except Exception as e:
        print("Error while inserting the new record :", repr(e))
        p1 = Response(1, "We can't add your report to the system.", None)
        return p1


def getShops(msg_received):
    organization_id = msg_received["organization_id"]
    select_query = '''SELECT * FROM shop where organization_id = %s''' % organization_id
    db_cursor.execute(select_query)
    row_headers = [x[0] for x in db_cursor.description]
    records = db_cursor.fetchall()
    json_data = []

    if len(records) == 0:
        p1 = Response(1, "No shops found.", None)
        return p1

    for result in records:
        json_data.append(dict(zip(row_headers, result)))
        print(json_data)

    return Response(0, "Success.", json_data)


def getAllShops():
    select_query = '''SELECT organization.name AS org_name, organization.logo AS logo, organization.description AS 
    description, shop.id AS id, shop.name, shop.address, shop.phonenumber, shop.location FROM organization INNER JOIN 
    shop ON organization.id = shop.organization_id'''
    db_cursor.execute(select_query)
    row_headers = [x[0] for x in db_cursor.description]
    records = db_cursor.fetchall()
    json_data = []

    if len(records) == 0:
        p1 = Response(1, "No shops found.", None)
        return p1

    for result in records:
        json_data.append(dict(zip(row_headers, result)))
        print(json_data)

    return Response(0, "Success.", json_data)


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
        return model.model_price.runArima(type[0], category, sub_category)
    elif type[0] == "quantity":
        model.model_quantity.runArima(type[1])
    elif type[0] == "sales":
        return model.model_sales.runArima(type[0], category, sub_category)
    elif type[0] == "import":
        return model.model_imports.runArima(type[0], category, sub_category)
    else:
        model.model_price.runArima(type[1])

    if len(0) == 0:
        return "failure"
    else:
        return "success"


app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)
