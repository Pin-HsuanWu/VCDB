import mysql.connector as m
import globals

def hop(destination):
    #get 目前 user 的相關資訊
    query = "SELECT * FROM user WHERE uid = '%s';" % globals.current_uid
    globals.vc_cursor.execute(query)
    userInfo = globals.vc_cursor.fetchone()

    if (userInfo[3] == None):  # 沒有 user 的 current_version 的紀錄
        print("Cannot find where you are!")
        return

    origin = str(userInfo[3])  # 起點
    
    query = "SELECT * FROM commit WHERE version = '%s';" % origin
    globals.vc_cursor.execute(query)
    originInfo = globals.vc_cursor.fetchone()
    originTime = originInfo[5]
    
    # get hop direction
    query = "SELECT * FROM commit WHERE version = '%s';" % destination
    globals.vc_cursor.execute(query)
    destinationInfo = globals.vc_cursor.fetchone()

    if (destinationInfo == None):  # 沒有 destination 的紀錄
        print("Cannot find the destination!")
        return

    destinationTime = destinationInfo[5]
    
    alterData = "SET foreign_key_checks = 0;\n"
    found = False
    hopCount = 0
    
    # 確認 hop 方向
    if (destinationTime < originTime):  # past
        # 中繼點
        relay = origin
        relayBranch = str(userInfo[1])

        while (relay != None):
            # 找出下個要去的點
            query = "SELECT * FROM commit WHERE version = '%s';" % relay
            globals.vc_cursor.execute(query)
            relayInfo = globals.vc_cursor.fetchone()

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
            # 找出下個要去的點
            query = "SELECT * FROM commit WHERE last_version = '%s';" % relay
            globals.vc_cursor.execute(query)
            relayInfo = globals.vc_cursor.fetchone()
            
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
        val = (destination, relayBranch, globals.current_uid)
        globals.vc_cursor.execute(update, val)
        globals.vc_connect.commit()

        # 執行更新
        globals.user_cursor.execute(alterData)

        print("Successfully hop and you hop", hopCount, "commit(s)!")
        
    else:
        print('Cannot find the destination because it is not on the same branch!')

# if __name__ == '__main__':
#     dest = "47b09edd"
#     hop(dest)