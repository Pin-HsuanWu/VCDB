import mysql.connector as m
import uuid
import os
import dump

def commit(userID, branchID, msg):
    
    # check if user can commit or not
    # get 目前 user 的相關資訊
    query = "SELECT * FROM user WHERE uid = userID;"
    vc_cur.execute(query)
    userInfo = vc_cur.fetchall()
    
    # get 目前 branch 的相關資訊
    query = "SELECT * FROM branch WHERE bid = branchID"
    vc_cur.execute(query)
    branchInfo = vc_cur.fetchall()
    
    userNode = userInfo[3]
    branchTail = branchInfo[2]
    
    if (userNode != branchTail):
        print("Please update to the newest version of the branch first!")
        return
        
    
    # dump
    newSQL = dump(user_cur)  # assume return file name
    oldSQL = branchID + '_dump.sql'  # assume in same folder and named bid_dump.sql
    
    # diff
    new = parse_sql_script(newSQL)
    old = parse_sql_script(oldSQL)
    
    upgrade = generate_sql_diff(old, new)
    downgrade = generate_sql_diff(new, old)
    
    
    # update commit table
    insert = "INSERT INTO commit (version, last_version, branch, upgrade, downgrade, msg) VALUES (%s, %s, %s, %s, %s, %s)"
    
    version = str(uuid.uuid4())[:8]  # uuid (八位數的亂數)
    last_version = branchTail
    
    val = (version, last_version, branchID, upgrade, downgrade, msg)
    vc_cur.execute(insert, val)
    
    # update branch table
    update = "UPDATE branch SET tail = (%s) WHERE bid = branchID;"
    val = version  # tail 記錄 version
    vc_cur.execute(update, val)
    
    # update user table
    update = "UPDATE user SET current_version = (%s), current_branch = branchID WHERE uid = userID;"
    val = version
    vc_cur.execute(update, val)
    
    
    # delete old dump file and rename new dump file
    os.remove(oldSQL)
    os.rename(newSQL, oldSQL)
    
    print("Successfully commit")
    
    
    
if __name__ == '__main__':
    # connect setting
    user_connection = m.connect(host='localhost', user='root',password='userpw', database='userdb')
    user_cur = user_connection.cursor(buffered=True)
    
    vc_connection = m.connect(host='localhost', user='root',password='vcpw', database='vcdb')
    vc_cur = vc_connection.cursor(buffered=True)
    
    commit(user_cur, vc_cur, 'userID', 'branchID', 'msg')
    vc_connection.commit()
    
    # close connection
    user_cur.close()
    user_connection.close()
    vc_cur.close()
    vc_connection.close()
    
