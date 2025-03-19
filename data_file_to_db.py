import configparser
import sqlite3
import csv
import re

def get_config_vars():
    config = configparser.RawConfigParser()
    config.read_file(open(r'config'))

    return config.get('config', 'db_name') + ".db",\
        config.get('config', 'dataset_path') + '\\' + config.get('config', 'dataset_filename'),\
        config.get('config', 'table_name'),\
        config.get('config', 'data_types'),\
        config.get('config', 'primary_key')

def sanitize_headers(headers_to_sanitize):
    new = []

    for header in headers_to_sanitize:
        index = header.find('(')
        if index > 0:
            header = header[:index]

        header = re.sub('[^a-zA-Z _]+', '', header)
        header = header.replace(' ', '_')
        header = header.lower()

        if header[-1] == '_':
            header = header[0:-1]

        new.append(header)

    return new

def execute_statement(statements):
    con = sqlite3.connect(db_name)
    cur = con.cursor()

    for statement in statements:
        try:
            res = cur.execute(statement)
            con.commit()
        except Exception as e:
            print(e)
            return e

    return res

def create_table():
    headers_string = ', '.join(sanitized_headers)
    create_statement = f"CREATE TABLE {table_name} ({headers_string})"

    if primary_key != '':
        index = create_statement.find(primary_key) + len(primary_key)
        create_statement = create_statement[0:index] + " PRIMARY KEY" + create_statement[index:]

    execute_statement([create_statement])

def insert_data():
    insert_statements = []

    for row in data:
        val = [0] * len(row)
        for i, _ in enumerate(row):
            match data_types[i]:
                case 'string':
                    val[i] = f"""'{row[i]}'"""
                case 'int':
                    val[i] = int(row[i])
                case 'float':
                    val[i] = float(row[i])
                case _:
                    print("invalid data type found")

        insert_statements.append(f"""INSERT INTO {table_name} VALUES ({val[0]}, {val[1]}, {val[2]},
                                 {val[3]}, {val[4]}, {val[5]}, {val[6]}, {val[7]}, {val[8]},
                                 {val[9]}, {val[10]}, {val[11]})""")

    execute_statement(insert_statements)

def select_data():
    select_statement = f"SELECT * FROM {table_name}"
    return execute_statement([select_statement])

if __name__ == "__main__":
    db_name, dataset_path, table_name, data_types, primary_key = get_config_vars()
    data = []

    with open(dataset_path, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        headers = next(reader)

        sanitized_headers = sanitize_headers(headers)

        for line in reader:
            data.append(line)

    data_types = data_types.replace(' ', '')
    data_types = data_types.split(',')

    while 1:
        print()
        print("1 - Create Table")
        print("2 - Add Data")
        print("3 - Verify Data")
        print("0 - Exit")
        option = input("Enter number: ")

        match option:
            case '1':
                create_table()
            case '2':
                insert_data()
            case '3':
                data = select_data()
                for item in data:
                    print(item)
            case '0':
                print("Goodbye")
                break
            case _:
                print("Invalid option. Please try again.")
