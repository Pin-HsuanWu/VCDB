<<<<<<< HEAD
import mysql.connector as m
import os
import datetime

=======
import mysql.connector
import os
import datetime


>>>>>>> checkout
def dump(cur):

    # Data for Saving
    data = ""
<<<<<<< HEAD
    # data += "DROP DATABASE IF EXISTS `" + db + "`;\n"
    # data += "CREATE DATABASE `" + db + "`;\n"
    # data += "USE `" + db + "`;\n"
    # data += "\n\n"
=======
>>>>>>> checkout

    # Getting all table names
    cur.execute('SHOW TABLES;')
    tables = []
    for record in cur.fetchall():
        tables.append(record[0])

    for table in tables:
<<<<<<< HEAD
        # data += "DROP TABLE IF EXISTS `" + str(table) + "`;"

        cur.execute("SHOW CREATE TABLE `" + str(table) + "`;")
        data += "\n" + str(cur.fetchone()[1]) + ";\n\n"


    # Setting for saving db
    now = datetime.datetime.now()
    path = "../branch_tail_schema"
    filename = str("backup_" + now.strftime("%Y%m%d_%H%M") + ".sql")

    file = open(os.path.join(path, filename),"w")
    file.writelines(data)
    file.close()

    #print("Successfully dump " + filename)
    
    return filename
    
    
    
if __name__ == '__main__':
    # Connect to db
    connection = m.connect(host='localhost', user='root',password='0000', database='userdb')
    cur = connection.cursor(buffered=True)
    
    dump(cur)
    
    # Close connection
    cur.close()
    connection.close()
=======
        cur.execute("SHOW CREATE TABLE `" + str(table) + "`;")
        data += "\n" + str(cur.fetchone()[1]) + ";\n\n"

    # Setting for saving db
    now = datetime.datetime.now()
    filename = str("tmpfile" + ".sql")

    file = open(filename, "w")
    file.writelines(data)
    file.close()

    print("Successfully dump " + filename)

    return filename


#dump(user_cursor)
>>>>>>> checkout
