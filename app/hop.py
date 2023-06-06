import mysql.connector as m


def hop(user_connection, vc_connection, user_cur, vc_cur, userID, destination):
    
    # get 目前 user 的相關資訊
    query = "SELECT * FROM user WHERE uid = '%s';" % userID
    vc_cur.execute(query)
    userInfo = vc_cur.fetchone()

    if (userInfo[3] == None):  # 沒有 user 的 current_version 的紀錄
        print("Cannot find where you are!")
        return

    origin = str(userInfo[3])  # 起點
    
    query = "SELECT * FROM commit WHERE version = '%s';" % origin
    vc_cur.execute(query)
    originInfo = vc_cur.fetchone()
    originTime = originInfo[5]
    print(originTime)
    
    # get hop direction
    query = "SELECT * FROM commit WHERE version = '%s';" % destination
    vc_cur.execute(query)
    destinationInfo = vc_cur.fetchone()

    if (destinationInfo == None):  # 沒有 destination 的紀錄
        print("Cannot find the destination!")
        return

    destinationTime = destinationInfo[5]
    print(destinationTime)
    
    alterData = "SET foreign_key_checks = 0;\n"
    found = False
    hopCount = 0
    
    # 確認 hop 方向
    if (destinationTime < originTime):  # past
        relay = origin
        relayBranch = str(userInfo[1])
        # alterData += str(originInfo[4]) + "\n"  # downgrade
        # hopCount += 1

        # # 中繼點
        # relay = str(originInfo[2])
        # relayBranch = str(userInfo[1])

        # if (destination == relay):
        #     found = True

        while (relay != None):
            print("relay: ", relay)
            # 找出下個要去的點
            query = "SELECT * FROM commit WHERE version = '%s';" % relay
            vc_cur.execute(query)
            relayInfo = vc_cur.fetchone()

            if (relayInfo == None): break

            alterData += str(relayInfo[4]) + "\n"  # downgrade
            relay = str(relayInfo[2])
            relayBranch = str(relayInfo[1])

            hopCount += 1
            
            if (destination == relay):
                found = True
                break
            
    elif (destinationTime > originTime):  # future
        # 中繼點
        relay = origin
        relayBranch = str(userInfo[1])
    
        while (relay != None):
            print("relay: ", relay)
            # 找出下個要去的點
            query = "SELECT * FROM commit WHERE last_version = '%s';" % relay
            vc_cur.execute(query)
            relayInfo = vc_cur.fetchone()
            
            if (relayInfo == None):  break
            
            alterData += str(relayInfo[3]) + "\n"  # upgrade
            relay = str(relayInfo[0])
            relayBranch = str(relayInfo[1])

            hopCount += 1
            
            if (destination == relay):
                found = True
                break
    else:
        print('You do not need to hop! You are here already!')
        return
    
    
    # 確認是否可以更新
    if (found == True):
        # 更新 vc 的 user table
        update = "UPDATE user SET current_version = (%s), current_bid = (%s) WHERE uid = (%s);"
        val = (destination, relayBranch, userID)
        vc_cur.execute(update, val)
        vc_connection.commit()

        # 執行更新
        print(alterData)
        user_cur.execute(alterData)
        user_connection.commit()
        
    else:
        print('Cannot find the version!')

    print("hopCount: ", hopCount)
    

if __name__ == '__main__':
    
    # connect setting
    user_connection = m.connect(host='localhost', user='root',password='0000', database='userdb')
    user_cur = user_connection.cursor(buffered=True)
    
    vc_connection = m.connect(host='localhost', user='root',password='0000', database='vcdb')
    vc_cur = vc_connection.cursor(buffered=True)

    # test data
    userID = '1'
    destination = '8f3954ea'
    
    hop(user_connection, vc_connection, user_cur, vc_cur, userID, destination)
    
    # close connection
    user_cur.close()
    user_connection.close()
    vc_cur.close()
    vc_connection.close()
	