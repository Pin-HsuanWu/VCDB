# this file is a GUI.py mock-up, aiming at testing whether the function.py is going to work in GUI.py using all global variables.

# import globals
from checkout import checkout
import mysql.connector
import globals


def init_connections():
    print("initing")
    connection1 = mysql.connector.connect(
        user="root", password="tubecity0212E_", host='127.0.0.1', port="3306", database='vcdb')
    print("VCDB connected.")

    globals.connection1 = mysql.connector.connect(
        user="root", password="mypassword", host='127.0.0.1', port="3306", database='vcdb')
    print("VCDB connected.")
    globals.vc_cursor = globals.connection1.cursor()

    globals.connection2 = mysql.connector.connect(
        user="root", password="tubecity0212E_", host='127.0.0.1', port="3306", database='userdb')
    print("user DB connected.")
    globals.user_cursor = globals.connection2.cursor()

    globals.userid = "testtt"


# import the function.py you want to test

# write down tests
init_connections()
checkout("func2", False)
# checkout("func3", False)
