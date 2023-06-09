import mysql.connector

# first we declare that we will need these global vars in all other files
def globalvar_initiation():
    global userdb_name
    global db_connect
    global db_cursor
    global current_uid
    global current_version
    global current_bid
    global vc_connect
    global user_connect
    global vc_cursor
    global user_cursor
    global vcdb_name

    userdb_name = None
    db_connect = None
    db_cursor = None
    current_version = None
    current_bid = None
    vc_connect = None
    user_connect = None
    vc_cursor = None
    user_cursor = None
    current_uid = None
    vcdb_name = None

globalvar_initiation()