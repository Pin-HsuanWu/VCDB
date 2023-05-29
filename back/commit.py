import mysql.connector as m
import uuid
import os

def commit(userID, branchID, msg):
    
    # connect setting
    # assume we have connected to userDB & vcDB
    user_connection = m.connect(host='localhost', user='root',password='userpw', database='userdb')
    user_cur = user_connection.cursor(buffered=True)
    
    vc_connection = m.connect(host='localhost', user='root',password='vcpw', database='vcdb')
    vc_cur = vc_connection.cursor(buffered=True)
    
    # dump
    newSQL = dump(user_cur)  # assume return file name
    oldSQL = branchID + '_dump.sql'  # assume in same folder and named bid_dump.sql
    
    # diff
    new = parse_sql_script(newSQL)
    old = parse_sql_script(oldSQL)
    
    upgrade = generate_sql_diff(old, new)
    downgrade = generate_sql_diff(new, old)
    
    # get 目前 branch 的相關資訊
    query = "SELECT * FROM branch WHERE bid = 'branchID'"
    vc_cur.execute(query)
    branchInfo = vc_cur.fetchall()
    
    # update commit table    # 目前的 commit table 沒有 branch 的 column
    insert = "INSERT INTO commit (cid, version, last_version, branch, upgrade, downgrade, msg) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    
    version = str(uuid.uuid4())  # uuid (亂數)
    last_version = branchInfo[2]  # 同 branch 的 head
    
    val = (cid, version, last_version, branchID, upgrade, downgrade, msg)
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
    
    
if __name__ == '__main__':
    commit('userID', 'branchID', 'msg')
