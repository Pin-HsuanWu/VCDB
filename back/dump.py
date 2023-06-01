import mysql.connector as m
import os
import datetime

def dump(cur):

    # Data for Saving
    data = ""
    # data += "DROP DATABASE IF EXISTS `" + db + "`;\n"
    # data += "CREATE DATABASE `" + db + "`;\n"
    # data += "USE `" + db + "`;\n"
    # data += "\n\n"

    # Getting all table names
    cur.execute('SHOW TABLES;')
    tables = []
    for record in cur.fetchall():
        tables.append(record[0])

    for table in tables:
        # data += "DROP TABLE IF EXISTS `" + str(table) + "`;"

        cur.execute("SHOW CREATE TABLE `" + str(table) + "`;")
        data += "\n" + str(cur.fetchone()[1]) + ";\n\n"


    # Setting for saving db
    now = datetime.datetime.now()
    filename = str("backup_" + now.strftime("%Y%m%d_%H%M") + ".sql")

    file = open(filename,"w")
    file.writelines(data)
    file.close()

    print("Successfully dump " + filename)
    
    return filename
    
    
    
if __name__ == '__main__':
    # Connect to db
    connection = m.connect(host='localhost', user='root',password='userpw', database='userdb')
    cur = connection.cursor(buffered=True)
    
    dump(cur)
    
    # Close connection
    cur.close()
    connection.close()