# first we declare that we will need these global vars in all other files
def globalvar_initiation():
    global userdb_name
    global userid
    global db_connect
    global db_cursor
    global current_version
    global current_branch
    global connection1
    global connection2
    global vc_cursor
    global user_cursor

    userid = None
    userdb_name = None
    db_connect = None
    db_cursor = None
    current_version = None
    current_branch = None
    connection1 = None
    connection2 = None
    vc_cursor = None
    user_cursor = None


globalvar_initiation()