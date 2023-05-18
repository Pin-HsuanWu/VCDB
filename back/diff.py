#!/usr/bin/env python
# coding: utf-8

# # Read SQL file

# In[2]:


def readSqlFile(filename):
    # Open and read the file as a single buffer
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()

    # all SQL commands (split on ';')
    sqlCommands = sqlFile.split(';')

    # Execute every command from the input file
    for command in sqlCommands:
        print(command)
        
    return sqlFile


# In[3]:


commit1 = readSqlFile('inputdata_withoutdrop.sql')


# In[4]:


commit2 = readSqlFile('inputdata2_withoutdrop.sql')


# # Compare the difference with the previous commit

# In[5]:


import re

def parse_sql_script(sql_script):
    table_dict = {}

    # Extract table name and column definitions
    pattern = r"CREATE TABLE `(\w+)` \((.*?)\)(?:\s*ENGINE.*?)?;"
    matches = re.findall(pattern, sql_script, re.DOTALL | re.MULTILINE)

    for match in matches:
        table_name = match[0]
        column_matches = re.findall(r"`([^`]+)` ([^,]+)", match[1])

        if not column_matches:
            raise ValueError(f"Invalid column definitions for table: {table_name}")

        column_dict = {column[0]: column[1].strip() for column in column_matches}
        table_dict[table_name] = column_dict

    return table_dict


# In[6]:


# Slice the sql into scripts of create table
commit1_dict = parse_sql_script(commit1)
commit2_dict = parse_sql_script(commit2)


# In[7]:


commit1_dict


# In[8]:


commit2_dict


# # Turn SQL file into upgrade code

# 加入PrimaryKey, Foreign Key, Foreign Constraint(順序)問題(可能獨立出來做？)

# In[9]:


def generate_sql_diff(commit1_dict, commit2_dict):
    sql_script = ""

    # Get the set of all table names from both commits
    all_tables = set(commit1_dict.keys()).union(commit2_dict.keys())

    # Compare table attributes for each table
    for table_name in all_tables:
        if table_name not in commit1_dict:
            # Table added in commit 2
            attributes2 = commit2_dict[table_name]
            attribute_str = ", ".join([f"{name} {definition}" for name, definition in attributes2.items()])
            sql_script += f"CREATE TABLE `{table_name}` ({attribute_str});\n"
        elif table_name not in commit2_dict:
            # Table deleted in commit 2
            sql_script += f"DROP TABLE `{table_name}`;\n"
        else:
            attributes1 = commit1_dict[table_name]
            attributes2 = commit2_dict[table_name]

            # Compare attributes for the table
            for attribute_name, attribute_definition in attributes1.items():
                if attribute_name not in attributes2:
                    # Attribute deleted in commit 2
                    sql_script += f"ALTER TABLE `{table_name}` DROP COLUMN `{attribute_name}`;\n"
                elif attribute_definition != attributes2[attribute_name]:
                    # Attribute changed in commit 2
                    sql_script += f"ALTER TABLE `{table_name}` MODIFY COLUMN `{attribute_name}` {attributes2[attribute_name]};\n"

            # Check for new attributes added in commit 2
            for attribute_name, attribute_definition in attributes2.items():
                if attribute_name not in attributes1:
                    sql_script += f"ALTER TABLE `{table_name}` ADD `{attribute_name}` {attribute_definition};\n"

    return sql_script


# In[10]:


print(generate_sql_diff(commit1_dict, commit2_dict))


# In[ ]:


# Upgrade -> generate_sql_diff(commit1_dict, commit2_dict)
# Downgrade -> generate_sql_diff(commit2_dict, commit1_dict)


# In[11]:


# Example usage:
commit3_dict = {
    'course': {'Name': 'varchar(20) NOT NULL', 'Teacher': 'varchar(20) NOT NULL'},
    'student': {'Id': 'varchar(20) NOT NULL', 'Name': 'varchar(20) NOT NULL'}
}

commit4_dict = {
    'course': {'Name': 'varchar(20) NOT NULL', 'Teacher': 'varchar(20) NOT NULL'},
    'student': {'Id': 'varchar(20) NOT NULL', 'Name': 'varchar(30) NOT NULL', 'Grade': 'int(11) NOT NULL'},
    'exam': {'Math': 'int', 'Chinese':'float'}
}

print("Upgrade: \n"+ generate_sql_diff(commit3_dict, commit4_dict))
print("Downgrade: \n"+ generate_sql_diff(commit4_dict, commit3_dict))

