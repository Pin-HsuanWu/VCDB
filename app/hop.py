import mysql.connector as m


def hop(user_cur, vc_cur, userID, destination):
    
    # get 目前 user 的相關資訊
    query = "SELECT * FROM user WHERE uid = userID;"
    vc_cur.execute(query)
    userInfo = vc_cur.fetchall()
    origin = str(userInfo[3])  # 起點
    
    query = "SELECT * FROM commit WHERE version = origin;"
    vc_cur.execute(query)
    originInfo = vc_cur.fetchall()
    originTime = originInfo[5]
    
    # get hop direction
    query = "SELECT * FROM commit WHERE version = destination;"
    vc_cur.execute(query)
    destinationInfo = vc_cur.fetchall()
    destinationTime = destinationInfo[5]
    
    alterData = ""
    found = False
    
    # 確認 hop 方向
    if (destinationTime < originTime):  # past
        alterData += str(originInfo[4]) + "\n"  # downgrade
        
        # 中繼點
        relay = str(originInfo[2])
        relayBranch = str(userInfo[1])
        
        while (relay != None):
            # 找出下個要去的點
            query = "SELECT * FROM commit WHERE version = relay"
            vc_cur.execute(query)
            
            relayInfo = vc_cur.fetchone()
            alterData += str(relayInfo[4]) + "\n"  # downgrade
            relay = str(relayInfo[2])
            relayBranch = str(relayInfo[1])
            
            if (destination == relay):
                found = True
                break
            
    elif (destinationTime > originTime):  # future
        alterData += str(originInfo[3]) + "\n"  # upgrade
        
        # 中繼點
        relay = origin
        relayBranch = str(userInfo[1])
    
        while (relay != None):
            # 找出下個要去的點
            query = "SELECT * FROM commit WHERE last_version = relay"
            vc_cur.execute(query)
            
            relayInfo = vc_cur.fetchone()
            
            if (relayInfo == []):
                break
            
            alterData += str(relayInfo[3]) + "\n"  # upgrade
            relay = str(relayInfo[0])
            relayBranch = str(relayInfo[1])
            
            if (destination == relay):
                found = True
                break
    else:
        print('You do not need to hop! You are here already!')
        return
    
    
    # 確認是否可以更新
    if (found == True):
        # 執行更新
        user_cur.execute(alterData)
        
        # 更新 vc 的 user table
        update = "UPDATE user SET current_version = (%s), current_branch = (%s) WHERE uid = userID;"
        val = (destination, relayBranch)
        vc_cur.execute(update, val)
    
    else:
        print('Cannot find the version!')
    

if __name__ == '__main__':
    
    # connect setting
    user_connection = m.connect(host='localhost', user='root',password='0000', database='userdb')
    user_cur = user_connection.cursor(buffered=True)
    
    vc_connection = m.connect(host='localhost', user='root',password='0000', database='vcdb')
    vc_cur = vc_connection.cursor(buffered=True)
    
    hop(user_cur, vc_cur, 'userID', 'destination')
    user_connection.commit()
    vc_connection.commit()
    
    # close connection
    user_cur.close()
    user_connection.close()
    vc_cur.close()
    vc_connection.close()
	