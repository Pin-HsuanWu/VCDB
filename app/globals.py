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
    global current_uid
    global user_host
    global user_pwd
    global user_port
    global user_name

    userdb_name = None
    current_version = None
    current_bid = None
    vc_connect = None
    user_connect = None
    vc_cursor = None
    user_cursor = None
    current_uid = None
    database_name = 'vcdb'
    user_host = None
    user_pwd = None
    user_port = None
    user_name = None


globalvar_initiation()