# this file is a GUI.py mock-up, aiming at testing whether the function.py is going to work in GUI.py using all global variables.

# import globals
# from checkout import checkout
import merge
import mysql.connector
import globals
import os
from dotenv import load_dotenv
load_dotenv()
import sys
import commit

def init_connections():
    print("start initing connections.")

    # get 2 connections
    user = "root"
    pwd = "tubecity0212E_"

    connection1 = mysql.connector.connect(
        user=user, password=pwd, host='127.0.0.1', port="3306", database='vcdb')
    globals.vc_connect = connection1
    globals.vc_cursor = connection1.cursor()
    print("VCDB connected.")

    connection2 = mysql.connector.connect(
        user=user, password=pwd, host='127.0.0.1', port="3306", database='userdb')
    globals.user_connect = connection2
    globals.user_cursor = connection2.cursor()
    print("user DB connected.")

    # insert data for testing
    # query = "insert into user values (%s, %s, %s, %s, %s);"
    # values = ["test2", "aMember", "member.com", "testtt2", "func2"]
    # globals.vc_cursor.execute(query, values)
    # globals.connection2.commit()
    # globals.userid = "test2"
    globals.current_uid = "dbd55daf-e57a-48b8-b9e8-66da27651986"
    globals.current_bid = 8
    globals.user_host = '127.0.0.1'
    
    globals.userdb_name = 'userdb'
    globals.user_name = 'root'
    globals.user_pwd = 'tubecity0212E_'

    print("vc_con ", globals.vc_connect,"vc_cur", globals.vc_cursor,"user_cur", globals.user_cursor)
    return




# test functions
# checkout("func1", False)
# checkout("func3", False)
# checkout("func3", True)
if __name__ == '__main__':
    # from tkinter import messagebox
    init_connections()
    try:
        print(merge.merge('branch9', 'main'))
        #自己在branch9, 把main merge近來。
    except:
        # print("=================================")
        # print("merge error: ", e)
        # messagebox("merge", e)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("============================================")
        print("Error file name: ", fname)
        print("Error Type: ", exc_type)
        print("Error occurs in line:", exc_tb.tb_lineno)
        print("Error msg:", exc_obj)
        print("============================================")
