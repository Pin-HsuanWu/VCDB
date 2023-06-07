import mysql.connector as m
import os
import datetime
import globals
import sys
import os

def dump(cur):
    try:
        # Data for Saving
        data = ""
        # data += "DROP DATABASE IF EXISTS `" + db + "`;\n"
        # data += "CREATE DATABASE `" + db + "`;\n"
        # data += "USE `" + db + "`;\n"
        # data += "\n\n"

        # Getting all table names
        newuserconn = m.connect(host=globals.user_host, database=globals.userdb_name, user=globals.user_name, passwd=globals.user_pwd)
        cur = newuserconn.cursor()
        globals.user_cursor = newuserconn.cursor()
        globals.user_connect = newuserconn
        globals.user_cursor.execute('use userdb;')
        globals.user_cursor.execute('SHOW TABLES;')
        tables = []
        
        for record in globals.user_cursor.fetchall():
            tables.append(record[0])

        for table in tables:
            # data += "DROP TABLE IF EXISTS `" + str(table) + "`;"

            globals.user_cursor.execute("SHOW CREATE TABLE `" + str(table) + "`;")
            data += "\n" + str(globals.user_cursor.fetchone()[1]) + ";\n\n"


        # Setting for saving db
        now = datetime.datetime.now()
        path = "./branch_tail_schema"
        filename = str("backup_" + now.strftime("%Y%m%d_%H%M") + ".sql")

        file = open(os.path.join(path, filename),"w")
        file.writelines(data)
        file.close()

        #print("Successfully dump " + filename)
        
        return filename

    except:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("============================================")
        print("Error file name: ", fname)
        print("Error Type: ", exc_type)
        print("Error occurs in line:", exc_tb.tb_lineno)
        print("Error msg:", exc_obj)
        print("============================================")


    
    
    
# if __name__ == '__main__':
#     # Connect to db
#     connection = m.connect(host='localhost', user='root',password='secure1234', database='db_class')
#     cur = connection.cursor(buffered=True)
    
#     dump(cur)
    
#     # Close connection
#     cur.close()
#     connection.close()