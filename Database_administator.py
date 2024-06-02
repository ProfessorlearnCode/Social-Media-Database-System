import pyodbc
import pandas as pd
import time
import os
import sys
import pwinput

def user_authorization():
    """
    The function `user_authorization` allows a user to input their username and password for
    authorization, with a limit of 3 attempts before exiting the program.
    :return: The function `user_authorization()` returns a boolean value `True` if the user enters the
    correct username ('admin' or 'professor') and password (0000). If the user fails to authenticate
    within 3 attempts, the program will exit without returning any value.
    """
    print("--------------------------------------------------------------")
    print("USER AUTHORIZATION")
    print("--------------------------------------------------------------")
    
    authorization_counter = 0
    while (authorization_counter < 3):
        try:
            username = input("Enter your username: ")
            password = int(pwinput.pwinput('Enter your password: ','*'))
            if (username == 'admin' and password == 0000) and (username == 'professor' and password == 0000):
                print(f"Welcome to Database Administrator: {username}")
                return True
            else:
                print("\nIncorrect Username or Password. Please try again.")
                authorization_counter = authorization_counter + 1
                print(f"Attempts remaining: {3 - authorization_counter}\n")
        
        except ValueError:
            print("\nIncorrect Username or Password. Please try again.")
            authorization_counter = authorization_counter + 1
            print(f"Attempts remaining: {3 - authorization_counter}\n")
                    
    print("Too many attempts!\nExiting the program")
    sys.exit()        

def connection_to_server():
    """
    The function `connection_to_server` establishes a connection to a SQL Server using pyodbc in Python.
    :return: The `Connection_string` object is being returned from the `connection_to_server` function.
    """
    try:
        Connection_string = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};' +
                                           'Server=DESKTOP-95OCRCQ;' +
                                           'Trusted_Connection=yes;')
        
        time.sleep(1)
        print("\nConnection to Server Successful 👍!\n")
        
        return Connection_string
        
    except pyodbc.Error as error_message:
        print("Connection Failed to the server ❌", error_message)

def show_databases(Connection_str):
    """
    The function `show_databases` retrieves and displays the names of databases in a given server using
    a SQL query.
    
    :param Connection_str: The `Connection_str` parameter in the `show_databases` function should be a
    connection string that contains the necessary information to establish a connection to a database
    server. This connection string typically includes details such as the server address, database name,
    authentication credentials (username and password), and any other required parameters
    """
    cursor = Connection_str.cursor()
    
    SQL_query = "SELECT name FROM sys.databases"
    cursor.execute(SQL_query)
    
    print("Databases in the server:")
    rows = cursor.fetchall()
    
    for row in rows:
        print('->', row[0])
    cursor.close()
                   
def change_database(connection_str):
    """
    The function `change_database` switches the connection to a different database using the provided
    connection string in Python.
    
    :param connection_str: The `connection_str` parameter in the `change_database` function is expected
    to be a connection string that contains the necessary information to establish a connection to a
    database. This connection string typically includes details such as the database server address,
    database name, authentication credentials, and any other required parameters to connect to
    :return: The function `change_database` returns the name of the database that the connection has
    been switched to.
    """
    
    cursor = connection_str.cursor()
    SQL_QUERY_DB = f"SELECT DB_NAME() as CurrentDB"
    cursor.execute(SQL_QUERY_DB)
    current_DB = cursor.fetchone()
    print(f"Currently Connected Database: {current_DB[0]}")
    database_name = input("Enter the name of the database you want to switch to: ")
    try:
        SQL_QUERY = f"USE {database_name}"
        cursor.execute(SQL_QUERY)
        
        time.sleep(1)
        print(f"Successfully Connected to {database_name} 👍")
        
        cursor.close()
        return database_name

    except pyodbc.Error as error_message:
        print("Failed to switch to the database ❌", error_message)

def show_tables(connection_str):
    """
    The function `show_tables` retrieves and displays the names of all base tables in a database using
    the provided connection string.
    
    :param connection_str: The `connection_str` parameter in the `show_tables` function is expected to
    be a connection string that contains the necessary information to establish a connection to a
    database. This connection string typically includes details such as the database driver, server
    address, database name, authentication credentials, and any other required parameters to
    """
    try:
        cursor = connection_str.cursor()
        
        cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'")
        
        tables = cursor.fetchall()
        
        print("Tables in the database:")
        for table in tables:
            print('->', table[0])
    
        cursor.close()
        
    except pyodbc.Error as error_message:
        print("Failed to retrieve the variable ❌", error_message)

def create_table(connection_str):
    """
    The function `create_table` takes a connection string as input, prompts the user to input a table
    name and attributes, then creates a table with the specified attributes in the database connected to
    the given connection string.
    
    :param connection_str: The `connection_str` parameter is typically a connection string that contains
    the information needed to establish a connection to a database. It usually includes details such as
    the database driver, server address, port, database name, username, and password
    """
    try:
        cursor = connection_str.cursor()
        
        table_name = input("Insert the name of the table you want to create: ")
        print("Adding attributes w/o constraints")
        try:
            attributes = input("Enter attributes separated by commas: ")
            
            SQL_QUERY = f'''CREATE TABLE {table_name}(
                            {attributes}
                            );'''
            cursor.execute(SQL_QUERY)
        except ValueError:
            print("Invalid Length Entered!")
        
        connection_str.commit()  
        
        cursor.close()
        
        print("Table Created Successfully 👍!")
    except pyodbc.Error as error_message:
        print("Failed to create your specified table ❌", error_message)
        
def show_column_names(connection_str, table_name):
    """
    The function `show_column_names` retrieves the column names of a specified table in a database using
    a given connection string.
    
    :param connection_str: The `connection_str` parameter is typically a connection string that contains
    the information needed to connect to a database. It usually includes details such as the database
    driver, server address, port, database name, username, and password. This string is used to
    establish a connection to the database before executing any SQL
    :param table_name: The `table_name` parameter in the `show_column_names` function is used to specify
    the name of the table for which you want to retrieve the column names. This function will query the
    database to get the column names of the specified table
    :return: The `show_column_names` function returns a list of column names from the specified table in
    the database connection. If an error occurs during the execution, it returns a tuple with an error
    message indicating the failure.
    """
    try:
      
        cursor = connection_str.cursor()
        DUMMY_SQL_QUERY = f"SELECT * FROM {table_name} WHERE 1=0"
        cursor.execute(DUMMY_SQL_QUERY)
        
        column_names=[]
        column_name_row = cursor.description
        for row in column_name_row:
            column_names.append(row[0])
            
        cursor.close()
        return column_names    
        
    except pyodbc.Error as error_message:
        return ("Failed to retrive the specified database ❌", error_message)
        
def Insertion(connection_str):
    """
    The `Insertion` function in Python allows users to insert values into a specified table in a
    database, handling cases where a timestamp column is present or not.
    
    :param connection_str: The `connection_str` parameter in the `Insertion` function is a connection
    string that is used to establish a connection to a database. This connection string contains
    information such as the database driver, server name, database name, authentication details, etc.,
    required to connect to the database. It is typically
    """
    try:
        table_name = input("Enter the name of the table you want to insert into? ")
        attribute_list = show_column_names(connection_str, table_name)
        
        cursor = connection_str.cursor()
        
        if 'CREATED_AT' in attribute_list:
            Values = input(f"Enter Values W.R.T Attributes:\n{'\t|\t'.join(attribute_list)}\n(separated by commas)\nValues: ")
            SQL_QUERY_wTime = f'''
                                INSERT INTRO {table_name} ({', '.join(attribute_list)})
                                VALUES ({Values}, GETDATE())
                                '''
            cursor.execute(SQL_QUERY_wTime)
            
        else:    
            Values = input(f"Enter Values W.R.T Attributes:\n{'\t|\t'.join(attribute_list)}\n(separated by commas)\nValues: ")
            SQL_QUERY_woTime = f'''INSERT INTO {table_name} ({', '.join(attribute_list)})
                            VALUES ({Values})
                        '''
            cursor.execute(SQL_QUERY_woTime)
        
        print("Values inserted Successfully 👍!")   
        
        connection_str.commit()
        cursor.close()
        
    except pyodbc.Error as error:
        print("Failed to insert values in the table ❌!", error)

def Updatation(connection_str):
    """
    The function `Updatation` takes user input for table name and update script, then executes an SQL
    query to update the specified table in the database.
    
    :param connection_str: The function `Updatation` takes a connection string as a parameter, which is
    used to establish a connection to a database. The user is prompted to enter the name of the table
    they want to update and the update script they want to execute on that table. The function then
    executes the update script
    """
    try:
        table_name = input("Enter the name of the table you want to update: ")
        update_instruction = input("Insert Update script: ")
        cursor = connection_str.cursor()
        
        SQL_QUERY = f'''Alter table {table_name}
                        {update_instruction}'''
        cursor.execute(SQL_QUERY)
        
        print("Instruction Update Successfully 👍!")
        
        connection_str.commit()
        cursor.close()
        
    except pyodbc.Error as error:
        print("Failed to update your query ❌", error)

def deletion(connection_str):
    """
    The `deletion` function takes a connection string as input, prompts the user for a table name and
    deletion condition, executes a SQL DELETE query using the provided inputs, and commits the
    transaction if successful.
    
    :param connection_str: The `deletion` function you provided takes a connection string as a
    parameter. This connection string is used to establish a connection to a database where the deletion
    operation will be performed
    """
    try:
        table_name = input("Enter the name of the table you want to delete from: ")
        condition = input("Enter the condition for deletion: ")
        
        cursor = connection_str.cursor()
        
        SQL_QUERY = f'''DELETE FROM {table_name}
                        WHERE {condition}'''
        
        cursor.execute(SQL_QUERY)
        
        print("Values deleted successfully 👍!")
        
        connection_str.commit()
        cursor.close()
    except pyodbc.Error as error:
        print("Failed to delete from the specifed table ❌!", error)

def table_truncation(connection_str):
    """
    The function `table_truncation` truncates a specified table in a database connection using SQL
    `TRUNCATE TABLE` or `DELETE FROM` based on the provided table name.
    
    :param connection_str: The `connection_str` parameter is typically a connection string that contains
    information needed to establish a connection to a database. It includes details such as the database
    driver, server address, database name, authentication credentials, etc. This connection string is
    used to create a connection to the database in order to perform operations
    """
    table_trunc = input("Enter the name of the table you want to truncate: ")
    
    cursor = connection_str.cursor()
    try:
        SQL_QUERY = f"TRUNCATE TABLE {table_trunc}"
        cursor.execute(SQL_QUERY)
        print("All contents deleted (truncated) Successfully 👍!")
        
    except pyodbc.Error as error_message:
        SQL_QUERY = f"DELETE FROM {table_trunc}"
        cursor.execute(SQL_QUERY)
    finally:
        connection_str.commit()  # Commit the truncation or deletion
        cursor.close()

def load_table_data(connection_str, table_name):
    """
    The function `load_table_data` reads data from a specified table in a database using a given
    connection string.
    
    :param connection_str: The `connection_str` parameter in the `load_table_data` function is typically
    a string that contains the connection information needed to connect to a database. This information
    usually includes details such as the database type, host, port, database name, username, and
    password
    :param table_name: The `table_name` parameter in the `load_table_data` function is used to specify
    the name of the table from which you want to load data. This function will construct a SQL query to
    select all columns from the specified table and then load the data into a pandas DataFrame using the
    provided `connection
    :return: The function `load_table_data` returns a DataFrame containing the data from the specified
    table in the database.
    """
    try:
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql(query, connection_str)
        return df
    
    except Exception as error:
        print("Failed to load table data ❌!", error)

def drop_table(connection_str):
    """
    The function `drop_table` drops a specified table in a database connection, handling potential
    errors related to primary and foreign keys.
    
    :param connection_str: The `connection_str` parameter is typically a connection string that contains
    the information needed to connect to a database. It usually includes details such as the database
    driver, server name, database name, authentication credentials, and any other necessary parameters
    to establish a connection to the database
    """
    try:
        print("WARNING: Drop a table with a defined PK or FK will result in an error\nConfigure in SSMS")
        table_name = input("Enter the name of the table you want to drop? ")
        cursor = connection_str.cursor()
        SQL_QUERY = f"DROP TABLE {table_name};"

        cursor.execute(SQL_QUERY)
        connection_str.commit()
        
        print("Table dropped successfully 👍!\n")
        cursor.close()
    
    except pyodbc.Error as error:
        print("Failed to drop the specified table ❌!", error)

def open_sql_file(connection_str):
    """
    The function `open_sql_file` reads and executes SQL commands from a specified file using a provided
    database connection string.
    
    :param connection_str: The `connection_str` parameter in the `open_sql_file` function is expected to
    be a connection string that is used to establish a connection to a database. This connection string
    is typically used to connect to a database using a specific driver, server address, database name,
    and authentication details. It is
    """
    try:
        file_path = input("Enter the path of the SQL file you want to execute: ")
        with open(file_path, 'r') as file:
            sql_commands = file.read()
        
        cursor = connection_str.cursor()
        cursor.execute(sql_commands)
        
        print(f"SQL file {file_path} executed successfully 👍!")
        
        connection_str.commit()
        
        cursor.close()
    
    except pyodbc.Error as error_message:
        print("Failed to open the sql file ❌!")
    
    except FileNotFoundError:
        print("SQL file not found. Please check the path and try again.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

def export_to_csv(connection_str, table_name, file_name):
    """
    This function exports data from a database table to a CSV file.
    
    :param connection_str: A connection string is a string that contains the information needed to
    connect to a database. It typically includes details such as the database server name, database
    name, authentication credentials, and any other necessary parameters to establish a connection to
    the database
    :param table_name: The `export_to_csv` function takes three parameters:
    :param file_name: The `export_to_csv` function you provided seems to be incomplete. It looks like
    you were about to provide some information about the parameters `connection_str`, `table_name`, and
    `file_name`, but the description is cut off. Could you please provide more details or let me know
    how I can
    """
    try:
        df = load_table_data(connection_str, table_name)
        if df is not None:
            df.to_csv(file_name, index=False)
            print(f"Data from {table_name} exported to {file_name} successfully 👍!")
            
    except Exception as error_message:
        print("Failed to export the csv file ❌", error_message)
        
        
def main():
    """
    The main function is the entry point of the program where the execution starts.
    """
    os.system('cls')
    
# This Python code is a console-based database manager program. It first checks for user authorization
# using the `user_authorization()` function. If the user is authorized, it clears the screen and
# displays a menu with various database management options.
    
    if(user_authorization()):
        os.system('cls')
        print('''
            Welcome to Database manager
            --------------------------------------------------------------
            Please choose an option:
            --------------------------------------------------------------
            1. Connect with the Server
            2. Show all present databases in the server
            3. Connect to a database
            4. Show all tables in the current database
            5. Create a new table in the current database
            6. Show the contents of the specified table
            7. Insert a value in the table
            8. Update a value in the table
            9. Delete a value in the table
            10. Delete all the entries within a table (Truncation)
            11. Drop a table
            12. Open SQL file
            13. Export to .csv file
            --------------------------------------------------------------
            m. Menu
            c. Clear
            q. Quit
            ''')
        
        print("--------------------------------------------------------------")
        while True:
            user_insert = input("Enter your choice: ")
            print("--------------------------------------------------------------\n")
        
            match user_insert:
                case '1':
                    connection_str = connection_to_server()
                    print("--------------------------------------------------------------\n")                   
                case '2':
                    try:
                        print('\n')
                        show_databases(connection_str)
                        print("--------------------------------------------------------------\n")
                        
                    except pyodbc.Error or UnboundLocalError as error_message:
                        print("Error Occurred\nPlease connect to the server first\n", error_message)
                        print("--------------------------------------------------------------\n")
                case '3':
                    try:
                        change_database(connection_str)
                        print("--------------------------------------------------------------\n")
                        
                    except pyodbc.Error or UnboundLocalError as error_message:
                        print("Error Occurred\nPlease connect to the server first\n", error_message)                
                        print("--------------------------------------------------------------\n")               
                case '4':
                    try:
                        show_tables(connection_str)
                        print("--------------------------------------------------------------\n")
                        
                    except pyodbc.Error or UnboundLocalError as error_message:
                        print("Error Occurred\nPlease connect to the server first\n", error_message)                
                        print("--------------------------------------------------------------\n")
                case '5':
                    try:
                        create_table(connection_str)
                        print("--------------------------------------------------------------\n")
                    except pyodbc.Error or UnboundLocalError as error_message:
                        print("Error Occurred\nPlease connect to the server first\n", error_message)
                        print("--------------------------------------------------------------\n")
                case '6':
                    try:
                        print("Viewing table Contents")
                        table_name = input("Import Table_name: ")
                        Table_DATA = load_table_data(connection_str, table_name)
                        print(f"{Table_DATA}")
                        print("--------------------------------------------------------------\n")
                        
                    except pyodbc.Error or UnboundLocalError as error_message:
                        print("Error Occurred\nPlease connect to the server first\n", error_message)                
                        print("--------------------------------------------------------------\n")
                case '7':
                    try: 
                        Insertion(connection_str)
                        print("--------------------------------------------------------------\n")
                        
                    except pyodbc.Error or UnboundLocalError as error_message:
                        print("Error Occurred\nPlease connect to the server first\n", error_message)
                        print("--------------------------------------------------------------\n")
                case '8':
                    try:
                        Updatation(connection_str)
                        print("--------------------------------------------------------------\n")
                        
                    except pyodbc.Error or UnboundLocalError as error_message:
                        print("Error Occurred\nPlease connect to the server first\n", error_message)
                        print("--------------------------------------------------------------\n")
                case '9':
                    try:
                        deletion(connection_str)
                        print("--------------------------------------------------------------\n")
                        
                    except pyodbc.Error as error_message:
                        print("Error Occurred\nPlease connect to the server first\n", error_message)                
                        print("--------------------------------------------------------------\n")
                case '10':
                    try:
                        table_truncation(connection_str)
                        print("--------------------------------------------------------------\n")
                        
                    except pyodbc.Error or UnboundLocalError as error_message:
                        print("Error Occurred\nPlease connect to the server first\n", error_message)
                        print("--------------------------------------------------------------\n")
                case '11':
                    try:
                        drop_table(connection_str)
                        print("--------------------------------------------------------------\n")
                    
                    except pyodbc.Error or UnboundLocalError as error_message:
                        print("Error Occurred\nPlease connect to the server first\n", error_message)
                        print("--------------------------------------------------------------\n")
                case '12':
                    try:
                        open_sql_file(connection_str)
                        print("--------------------------------------------------------------\n")
                        
                    except pyodbc.Error or UnboundLocalError as error_message:
                        print("Error Occurred\nPlease connect to the server first\n", error_message)
                        print("--------------------------------------------------------------\n")
                case '13':
                    try:
                        table_name = input("Enter the name of the table you want to export: ")
                        file_name = input("Enter the name of the CSV file (with .csv extension): ")
                        export_to_csv(connection_str, table_name, file_name)
                        print("--------------------------------------------------------------\n")
                        
                    except pyodbc.Error or UnboundLocalError as error_message:
                        print("Error Occurred\nPlease connect to the server first\n", error_message)                
                        print("--------------------------------------------------------------\n")
                case 'q':
                    connection_str.close()
                    time.sleep(1.5)
                    print("Connection Terminated!\nExiting the program")
                    print("--------------------------------------------------------------\n")
                    sys.exit()               
                case 'm':
                    print('''
                        --------------------------------------------------------------
                        Please choose an option:
                        --------------------------------------------------------------
                        1. Connect with the Server
                        2. Show all present databases in the server
                        3. Connect to a database
                        4. Show all tables in the current database
                        5. Create a new table in the current database
                        6. Show the contents of the specified table
                        7. Insert a value in the table
                        8. Update a value in the table
                        9. Delete a value in the table
                        10. Delete all the entries within a table (Truncation)
                        11. Drop a table
                        12. Open SQL file
                        13. Export to .csv file
                        --------------------------------------------------------------
                        m. Menu
                        c. Clear
                        q. Quit
                        ''')                       
                case 'c':
                    os.system('cls')                  
                case _:
                    print("Invalid Option. Please choose a valid option\n")
                    print("--------------------------------------------------------------\n")
                    pass
                    print("--------------------------------------------------------------\n")
    else:
        pass
if __name__ == "__main__":
    main()
