# this file is a GUI.py mock-up, aiming at testing whether the function.py is going to work in GUI.py using all global variables.

# import globals
from checkout import checkout
import mysql.connector
import globals
import os
from dotenv import load_dotenv
load_dotenv()



def init_connections():
    print("start initing connections.")

    # get 2 connections
    user = os.getenv("MYSQL_USER")
    pwd = os.getenv("MYSQL_PASSWORD")

    connection1 = mysql.connector.connect(
        user=user, password=pwd, host='127.0.0.1', port="3306", database=globals.vcdb_name)
    globals.vc_cursor = connection1.cursor()
    print("VCDB connected.")

    connection2 = mysql.connector.connect(
        user=user, password=pwd, host='127.0.0.1', port="3306", database='userdb')
    globals.user_cursor = connection2.cursor()
    print("user DB connected.")

    # insert data for testing
    # query = "insert into user values (%s, %s, %s, %s, %s);"
    # values = ["test2", "aMember", "member.com", "testtt2", "func2"]
    # globals.vc_cursor.execute(query, values)
    # globals.connection2.commit()
    globals.current_uid = "461870d7-3244-40e2-b403-727f3669a547"

    return

import utils

init_connections()

# test functions
utils.getAllBranchs()
# checkout("func1", False)
# checkout("func3", False)
# checkout("func3", True)


