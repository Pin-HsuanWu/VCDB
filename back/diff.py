import re

# Read SQL file
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



def parse_sql_script(sql_script):
    table_dict = {}
    current_table = ""
    current_attributes = {}

    create_table_pattern = re.compile(r"CREATE TABLE `(\w+)` \((.*?)\)(?:\s*ENGINE.*?)?;", re.DOTALL)
    attribute_pattern = re.compile(r"\n  `(.*?)` (.*?)(,|\n)", re.DOTALL)
    primary_key_pattern = re.compile(r"PRIMARY KEY \((.*?)\)", re.DOTALL)
    foreign_key_pattern = re.compile(r"CONSTRAINT `(.*?)` FOREIGN KEY \((.*?)\) REFERENCES `(.*?)` \((.*?)\)", re.DOTALL)

    matches = re.findall(create_table_pattern, sql_script)
    match = matches[1]
    for match in matches:
        current_table = match[0]
        current_attributes = {}

        attribute_matches = re.findall(attribute_pattern, match[1])
        for attribute_match in attribute_matches:
            attribute_name = attribute_match[0]
            attribute_definition = attribute_match[1].strip()
            # Check if attribute_match contains 'REFERENCES'
            if 'REFERENCES' in attribute_name:
                continue  # Skip and ignore the match
            current_attributes[attribute_name] = attribute_definition

        primary_key_match = re.search(primary_key_pattern, match[1])
        if primary_key_match:
            primary_key_columns = primary_key_match.group(1).strip('`').split(',')
            current_attributes['PRIMARY KEY'] = primary_key_columns

        foreign_key_matches = re.findall(foreign_key_pattern, match[1])
        for foreign_key_match in foreign_key_matches:
            constraint_name = foreign_key_match[0]
            foreign_key_columns = foreign_key_match[1]
            referenced_table = foreign_key_match[2]
            referenced_columns = foreign_key_match[3]
            if 'FOREIGN KEY' not in current_attributes:
                current_attributes['FOREIGN KEY'] = {}
            current_attributes['FOREIGN KEY'][foreign_key_columns.strip('`')] = {
                'CONSTRAINT': constraint_name,
                'REFERENCE_TABLE': referenced_table,
                'REFERENCE_COL': [col.strip('`') for col in referenced_columns.split(',')]
            }

        table_dict[current_table] = current_attributes

    return table_dict




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
            if 'PRIMARY KEY' in attributes2:
                primary_key_columns = ", ".join(attributes2['PRIMARY KEY'])
                attribute_str += f", PRIMARY KEY ({primary_key_columns})"
            if 'FOREIGN KEY' in attributes2:
                foreign_key = attributes2['FOREIGN KEY']
                for column, ref_info in foreign_key.items():
                    constraint_name = ref_info['CONSTRAINT']
                    referenced_table = ref_info['REFERENCE_TABLE']
                    referenced_columns = ", ".join(ref_info['REFERENCE_COL'])
                    attribute_str += f", CONSTRAINT `{constraint_name}` FOREIGN KEY (`{column}`) REFERENCES `{referenced_table}` (`{referenced_columns}`)"

            sql_script += f"CREATE TABLE `{table_name}` ({attribute_str});\n"
        elif table_name not in commit2_dict:
            # Table deleted in commit 2
            sql_script += f"DROP TABLE `{table_name}`;\n"
        else:
            attributes1 = commit1_dict[table_name]
            attributes2 = commit2_dict[table_name]

            # Compare attributes for the table
            for attribute_name, attribute_definition in attributes1.items():
                if attribute_name == 'FOREIGN KEY' or attribute_name == 'PRIMARY KEY':
                    continue
                if attribute_name not in attributes2:
                    # Attribute deleted in commit 2
                    sql_script += f"ALTER TABLE `{table_name}` DROP COLUMN `{attribute_name}`;\n"
                elif attribute_definition != attributes2[attribute_name]:
                    # Attribute changed in commit 2
                    sql_script += f"ALTER TABLE `{table_name}` MODIFY COLUMN `{attribute_name}` {attributes2[attribute_name]};\n"

            # Check for new attributes added in commit 2
            for attribute_name, attribute_definition in attributes2.items():
                if attribute_name not in attributes1 and attribute_name != 'PRIMARY KEY':
                    sql_script += f"ALTER TABLE `{table_name}` ADD COLUMN `{attribute_name}` {attribute_definition};\n"

            # Check for primary key differences
            if 'PRIMARY KEY' in attributes1 and 'PRIMARY KEY' in attributes2:
                if attributes1['PRIMARY KEY'] != attributes2['PRIMARY KEY']:
                    # Primary key changed in commit 2
                    sql_script += f"ALTER TABLE `{table_name}` DROP PRIMARY KEY;\n"
                    primary_key_columns = ", ".join(attributes2['PRIMARY KEY'])
                    sql_script += f"ALTER TABLE `{table_name}` ADD PRIMARY KEY ({primary_key_columns});\n"
                # Primary key remains the same, no action needed

            elif 'PRIMARY KEY' in attributes1 and 'PRIMARY KEY' not in attributes2:
                # Primary key removed in commit 2
                sql_script += f"ALTER TABLE `{table_name}` DROP PRIMARY KEY;\n"

            elif 'PRIMARY KEY' not in attributes1 and 'PRIMARY KEY' in attributes2:
                # Primary key added in commit 2
                primary_key_columns = ", ".join(attributes2['PRIMARY KEY'])
                sql_script += f"ALTER TABLE `{table_name}` ADD PRIMARY KEY ({primary_key_columns});\n"

            # Check for foreign key differences
            if 'FOREIGN KEY' in attributes1 and 'FOREIGN KEY' in attributes2:
                if attributes1['FOREIGN KEY'] != attributes2['FOREIGN KEY']:
                    # Foreign key changed in commit 2
                    foreign_keys_to_drop = set(attributes1['FOREIGN KEY'].keys()) - set(attributes2['FOREIGN KEY'].keys())
                    for foreign_key_name in foreign_keys_to_drop:
                        sql_script += f"ALTER TABLE `{table_name}` DROP FOREIGN KEY `{attributes1['FOREIGN KEY'][foreign_key_name]['CONSTRAINT']}`;\n"

                    foreign_key = attributes2['FOREIGN KEY']
                    for column, ref_info in foreign_key.items():
                        constraint_name = ref_info['CONSTRAINT']
                        referenced_table = ref_info['REFERENCE_TABLE']
                        referenced_columns = ", ".join(ref_info['REFERENCE_COL'])
                        sql_script += f"ALTER TABLE `{table_name}` ADD CONSTRAINT `{constraint_name}` FOREIGN KEY (`{column}`) REFERENCES `{referenced_table}` (`{referenced_columns}`);\n"
                # Foreign key remains the same, no action needed

            elif 'FOREIGN KEY' in attributes1 and 'FOREIGN KEY' not in attributes2:
                # Foreign key removed in commit 2
                foreign_keys_to_drop = attributes1['FOREIGN KEY'].keys()
                for foreign_key_name in foreign_keys_to_drop:
                    constraint_name = attributes1['FOREIGN KEY'][foreign_key_name]['CONSTRAINT']
                    sql_script += f"ALTER TABLE `{table_name}` DROP FOREIGN KEY `{constraint_name}`;\n"

            elif 'FOREIGN KEY' not in attributes1 and 'FOREIGN KEY' in attributes2:
                # Foreign key added in commit 2
                foreign_key = attributes2['FOREIGN KEY']
                for column, ref_info in foreign_key.items():
                    constraint_name = ref_info['CONSTRAINT']
                    referenced_table = ref_info['REFERENCE_TABLE']
                    referenced_columns = ", ".join(ref_info['REFERENCE_COL'])
                    sql_script += f"ALTER TABLE `{table_name}` ADD CONSTRAINT `{constraint_name}` FOREIGN KEY (`{column}`) REFERENCES `{referenced_table}` (`{referenced_columns}`);\n"

    return sql_script



# Upgrade -> generate_sql_diff(commit1_dict, commit2_dict)
# Downgrade -> generate_sql_diff(commit2_dict, commit1_dict)


# Example
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






