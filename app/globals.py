import mysql.connector

# first we declare that we will need these global vars in all other files
def globalvar_initiation():
    global userdb_name
    global db_connect
    global db_cursor
    global current_uid  # userid -> current_uid
    global current_version
    global current_bid  # current_branch -> current_bid
    global vc_connect
    global user_connect
    global vc_cursor
    global user_cursor
    global database_name

    userdb_name = None
    db_connect = None
    db_cursor = None
    current_version = None
    current_branch = None
    # vc_connect = None
    # user_connect = None
    # vc_cursor = None
    # user_cursor = None
    # current_uid = None
    current_bid = 1
    vc_connect = mysql.connector.connect(
        user="root", password="dbcourse", host='127.0.0.1', port="3306", database='vcdb')
    print("VCDB connected.")
    vc_cursor = vc_connect.cursor()

    user_connect = mysql.connector.connect(
    user="root", password="dbcourse", host='127.0.0.1', port="3306", database='userdb')
    print("user DB connected.")
    user_cursor = user_connect.cursor()

    current_uid = 'fakeuid'


globalvar_initiation()