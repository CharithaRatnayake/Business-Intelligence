import mysql.connector
import sys

# connect the database
try:
    db = mysql.connector.connect(host="localhost", user="root", passwd="")
    db_cursor = db.cursor()

    db_cursor.execute("SHOW DATABASES")
    databases = db_cursor.fetchall()
    print(databases)

    db_cursor.execute("use consumerprotection")
    db_cursor.execute("SHOW TABLES")
    databases = db_cursor.fetchall()
    print(databases)
except:
    print("Error connecting to the host. Please check your inputs.")
