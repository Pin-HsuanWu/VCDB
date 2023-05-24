import mysql.connector as m
import os
import datetime

# Connecting to db
db = 'user_dbname'
connection = m.connect(host='localhost', user='root',password='0000', database=db)
cur = connection.cursor(buffered=True)

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
print(filename)

FILE = open(filename,"w")
FILE.writelines(data)
FILE.close()

print("Success")