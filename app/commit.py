import mysql.connector as m
import uuid
import os
import datetime
from dump import dump
from diff import get_diff

def commit(vc_connection, user_cur, vc_cur, userID, branchID, msg):
    
    # check if user can commit or not
    # get 目前 user 的相關資訊
    query = "SELECT * FROM user WHERE uid = '%s';" % userID
    vc_cur.execute(query)
    userInfo = vc_cur.fetchone()
    # print("userInfo: ", userInfo)
    
    # get 目前 branch 的相關資訊
    query = "SELECT * FROM branch WHERE bid = '%s'" % branchID
    vc_cur.execute(query)
    branchInfo = vc_cur.fetchone()
    # print("branchInfo: ", branchInfo)
    
    if (userInfo[3] != ""):  # not initial commit
        userNode = userInfo[3]
        branchTail = branchInfo[2]
    
        if (userNode != branchTail):
            print("Please update to the newest version of the branch first!")
            return
        
    elif (userInfo[3] == "" and branchInfo[2] != ""):
        print("Please update to the newest version of the branch first!")
        return
        
    
    # dump
    path = "./branch_tail_schema"
    newSQL = dump(user_cur)  # assume return file name
    oldSQL = str(branchID) + '_dump.sql'  # assume in same folder and named bid_dump.sql
    
    # diff
    # new = parse_sql_script(newSQL)
    # old = parse_sql_script(oldSQL)
    # upgrade = generate_sql_diff(old, new)
    # downgrade = generate_sql_diff(new, old)
    

    if (branchInfo[2] != None):
        upgrade = get_diff(os.path.join(path, oldSQL), os.path.join(path, newSQL))
        downgrade = get_diff(os.path.join(path, newSQL), os.path.join(path, oldSQL))
        
    else:
        with open(os.path.join(path, newSQL)) as f:
            lines = f.readlines()
        upgrade = str(lines)
        downgrade = ""

    # check if upgrade = Null
    if (upgrade == ""):
        # os.remove(os.path.join(path, newSQL))
        print("Nothing to commit")
        return
    
    
    # update commit table
    insert = "INSERT INTO commit (version, bid, last_version, upgrade, downgrade, time, uid, msg) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    
    version = str(uuid.uuid4())[:8]  # uuid (八位數的亂數)
    if (branchInfo[2] != ""):
        last_version = branchTail
    else:
        last_version = ""
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    val = (version, branchID, last_version, upgrade, downgrade, time, userID, msg)
    vc_cur.execute(insert, val)
    
    # update branch table
    update = "UPDATE branch SET tail = (%s) WHERE bid = (%s);"
    val = (version, branchID)  # tail 記錄 version
    vc_cur.execute(update, val)
    
    # update user table
    update = "UPDATE user SET current_version = (%s), current_bid = (%s) WHERE uid = (%s);"
    val = (version, branchID, userID)
    vc_cur.execute(update, val)
    
    
    # delete old dump file and rename new dump file
    if (os.path.exists(os.path.join(path, oldSQL))):
        os.remove(os.path.join(path, oldSQL))
    os.rename(os.path.join(path, newSQL), os.path.join(path, oldSQL))
    
    print("Successfully commit")
    vc_connection.commit()
    
    
if __name__ == '__main__':
    # connect setting
    user_connection = m.connect(host='localhost', user='root',password='secure1234', database='db_class')
    user_cur = user_connection.cursor(buffered=True)
    
    vc_connection = m.connect(host='localhost', user='root',password='secure1234', database='vcdb')
    vc_cur = vc_connection.cursor(buffered=True)
    
    # test data
    userID = '3c30937d-fe2c-4f65-8cbf-619d5d6b7edb'
    branchID = '1'
    msg = '3rd commit'

    commit(vc_connection, user_cur, vc_cur, userID, branchID, msg)
    
    # close connection
    user_cur.close()
    user_connection.close()
    vc_cur.close()
    vc_connection.close()
    