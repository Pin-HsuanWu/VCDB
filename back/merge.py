from diff import read_sql_file ,parse_sql_script, generate_attribute_string, generate_sql_diff, get_diff
import mysql.connector
import uuid
import datetime
import time

"""
Database setup for test
"""
connection1 = mysql.connector.connect(
    user="root", password="dbcourse", host='127.0.0.1', port="3306", database='vcdb')
print("VCDB connected.")
cursor = connection1.cursor()

connection2 = mysql.connector.connect(
user="root", password="dbcourse", host='127.0.0.1', port="3306", database='userdb')
print("user DB connected.")
user_cursor = connection2.cursor()




# Add branch format for sql script in different branch
def branch_format(branch_list, branch_name):
    if branch_list[0].startswith(", \n"):
        branch_list[0] = branch_list[0][3:]
    
    branch_list.insert(0, f"/* {branch_name} */")
    branch_list.append("/************/\n")
    
    sql_script = '\n'.join(branch_list)
    return sql_script

# Generate attribute string for column definition
def check_table_conflicts(is_conflict, table_name, branch1_name, table1, branch2_name, table2):
    sql_script = ""
    
    conflicts = []
    attribute_str = ""
    nonconflict_attr_dict = {}

    # Change the order of two_tables
    two_tables = set(table1.keys()).union(table2.keys())
    constraint_keywords = ['PRIMARY KEY', 'CONSTRAINT_FOREIGN KEY', 'UNIQUE KEY', 'CONSTRAINT_CHECK']
    
    two_tables_without_keywords = set(table1.keys()).union(table2.keys())
    for keyword in constraint_keywords:
        two_tables_without_keywords.discard(keyword)
    
    two_tables_with_keywords = two_tables.difference(two_tables_without_keywords)
    two_tables_in_order = list(two_tables_without_keywords) + list(two_tables_with_keywords)

    # Check conflicts in column definitions
    for column_name in two_tables_in_order:
        # Column created
        if column_name not in table1:
            nonconflict_attr_dict.update({column_name: table2[column_name]})
        # Column deleted
        elif column_name not in table2:
            is_conflict = True
            attribute_str += branch_format([generate_attribute_string({column_name: table1[column_name]})], branch1_name)
            attribute_str += branch_format([''], branch2_name)
        # Column exists in both tables, check for conflicts
        else:
            # Column updated
            if table1[column_name] != table2[column_name]:
                is_conflict = True
                attribute_str += branch_format([generate_attribute_string({column_name: table1[column_name]})], branch1_name)
                attribute_str += branch_format([generate_attribute_string({column_name: table2[column_name]})], branch2_name)
            # Column remains the same
            else:
                nonconflict_attr_dict.update({column_name: table1[column_name]})
                
    if attribute_str:
        attribute_str = generate_attribute_string(nonconflict_attr_dict) +',\n'+ attribute_str
    else:
        attribute_str = generate_attribute_string(nonconflict_attr_dict)
    sql_script += f"CREATE TABLE `{table_name}` (\n{attribute_str});\n"
    return is_conflict, sql_script


# Check if there in any conflict when merging different branches
def check_branch_conflicts(branch1_name, branch1, branch2_name, branch2):
    is_conflict = False
    sql_script = ""
    all_tables = set(branch1.keys()).union(branch2.keys())
    
    # Check table conflicts
    for table_name in all_tables:
        # Table created
        if table_name not in branch1.keys():
            sql_script += generate_sql_diff({}, {table_name: branch2[table_name]})
            
        # Table deleted
        elif table_name not in branch2.keys():
            sql_script += branch_format([generate_sql_diff({}, {table_name: branch1[table_name]})], branch1_name)
            sql_script += branch_format([''], branch2_name)
            is_conflict = True
        
        # Table updated -> Check conflicts in table definitions
        else:
            if branch1[table_name] == branch2[table_name]:
                sql_script += generate_sql_diff({}, {table_name: branch1[table_name]})
            else:
                table_conflict = check_table_conflicts(is_conflict, table_name, branch1_name, branch1[table_name], branch2_name, branch2[table_name])
                is_conflict = table_conflict[0]
                sql_script += table_conflict[1]
        
    return is_conflict, sql_script


def merge_schema(commit1_dict, commit2_dict):
    merged_schema = {}

    # Merge tables from commit1
    for table_name, schema in commit1_dict.items():
        merged_schema[table_name] = schema

    # Merge tables from commit2
    for table_name, schema in commit2_dict.items():
        if table_name in merged_schema:
            # Table already exists, merge the schema
            merged_schema[table_name].update(schema)
        else:
            # Table doesn't exist, add it to the merged commit
            merged_schema[table_name] = schema

    return merged_schema




def merge(main_branch_name, target_branch_bame):
    # Read sql file by dump.py, then translate to json by diff.py
    # assume each branch's tail schema is stored in the following file name: {branchName}.sql
    main_branch_path = f"../branch_tail_schema/{main_branch_name}.sql"
    target_branch_path = f"../branch_tail_schema/{target_branch_bame}.sql"

    main_schema = read_sql_file(main_branch_path)
    target_schema = read_sql_file(target_branch_path)

    # Parse sql scripts into dictionary
    main_schema_dict = parse_sql_script(main_schema)
    target_schema_dict = parse_sql_script(target_schema)

    # check if 2 branch exists
    query = "SELECT name FROM branch;"
    cursor.execute(query)
    all_branch_names = cursor.fetchall()
    all_branch_names = ["%s" % x for x in all_branch_names]
    flag1 = False
    flag2 = False
    if main_branch_name in all_branch_names:
        flag1 = True
    if target_branch_bame in all_branch_names:
        flag2 = True
    if flag1 & flag2 == False:
        print("Cannot merge branches that does not exist.")

    # if conflict exists: show conflicts
    is_conflict = check_branch_conflicts(main_branch_name, main_schema_dict, target_branch_bame, target_schema_dict)
    if is_conflict[0]:
        print("Schema conflict exists between 2 branches as follows:")
        conflict_sql_script = is_conflict[1]
        print(conflict_sql_script)
    
    # if there is no conflict: merge 2 branches
    else:
        merged_schema_dict = merge_schema(main_schema_dict, target_schema_dict)
        downgrade = generate_sql_diff(main_schema_dict, merged_schema_dict)
        upgrade = generate_sql_diff(merged_schema_dict, main_schema_dict)

        msg = f"Merge {target_branch_bame} into {main_branch_name}"
        version = str(uuid.uuid4()) 


        # TODO!!!
        query = f"SELECT * FROM branch WHERE  name = '{main_branch_name}'"
        cursor.execute(query)
        branchInfo = cursor.fetchall()[0]
        print(branchInfo)
        last_version = branchInfo[2]
        print(f'last_version: {last_version}')

        # query = f"SELECT branch FROM commit WHERE version = '{main_branch_name}'"

        # query = f"SELECT * FROM branch WHERE name = '{main_branch_name}'"
        # cursor.execute(query)
        # branchInfo = cursor.fetchall()
        branchID = branchInfo[0]
        print(f'branchID: {branchID}')

        # Insert into commit table
        now = datetime.datetime.now()
        insert = "INSERT INTO commit (version, branch, last_version, upgrade, downgrade, time, msg) VALUES (%s, %s, %s, %s, %s, %s,%s, %s)"
        val = (version, last_version, branchID, upgrade, downgrade, now.strftime("%Y-%m-%d %H:%M:%S"), msg)
        cursor.execute(insert, val)

        # update branch table
        update = f"UPDATE branch SET tail = (%s) WHERE bid = {branchID};"
        val = version
        cursor.execute(update, val)

        print(f"Successfully merged {target_branch_bame} into {main_branch_name}!")
    return conflict_sql_script

if __name__ == '__main__':
    merge('branch1', 'branch2')
    


