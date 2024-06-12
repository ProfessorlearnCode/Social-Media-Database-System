import pyodbc
import pandas as pd
import time
import os
import sys
import pwinput

def custom_server_connect():  
    try:
        print("--------------------------------------------------------------")
        print("Custom server Connection")
        print("--------------------------------------------------------------")
        server_name = input("Enter the name of the server: ")
        connection_string = pyodbc.connect('Driver = {ODBC Driver 17 for SQL Server};' +
                                           f'Server = {server_name};' +
                                           'Trusted_Connection = yes;')
        
        time.sleep(1)
        print("\nConnection to Server Successful 👍!\n")
        
        return connection_string
      
    except pyodbc.Error as error_message:
        print("Connection Failed to the server ❌\n Please check your input", error_message)
  


def user_authorization():
   
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
   
    try:
        print("--------------------------------------------------------------")
        print("Connecting to the Server")
        print("--------------------------------------------------------------")
        Connection_string = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};' +
                                           'Server=DESKTOP-95OCRCQ;' +
                                           'Trusted_Connection=yes;')
        
        time.sleep(1)
        print("\nConnection to Server Successful 👍!\n")
        
        return Connection_string
        
    except pyodbc.Error as error_message:
        print("Connection Failed to the server ❌", error_message)

def show_databases(Connection_str):
 
    print("--------------------------------------------------------------")
    print("Showing Present Databases")
    print("--------------------------------------------------------------")
    
    cursor = Connection_str.cursor()
    
    SQL_query = "SELECT name FROM sys.databases"
    cursor.execute(SQL_query)
    
    print("Databases in the server:")
    rows = cursor.fetchall()
    
    for row in rows:
        print('->', row[0])
    cursor.close()
                   
def change_database(connection_str):
  
    print("--------------------------------------------------------------")
    print("Changing currently connected database")
    print("--------------------------------------------------------------")
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

    try:
        print("--------------------------------------------------------------")
        print("Showing tables present in the Current database")
        print("--------------------------------------------------------------")
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

    try:
        print("--------------------------------------------------------------")
        print("Creating a new table")
        print("--------------------------------------------------------------")
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

    try:
        print("--------------------------------------------------------------")
        print("Displaying attributes of a table")
        print("--------------------------------------------------------------")
      
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

    try:
        print("--------------------------------------------------------------")
        print("Inserting values in the table")
        print("--------------------------------------------------------------")
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

    print("--------------------------------------------------------------")
    print("Updating/Altering data in the database")
    print("--------------------------------------------------------------")
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

    try:
        print("--------------------------------------------------------------")
        print("Deleting data in the database")
        print("--------------------------------------------------------------")
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

    table_trunc = input("Enter the name of the table you want to truncate: ")
    print("--------------------------------------------------------------")
    print("Truncating a table data")
    print("--------------------------------------------------------------")
    
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
    
    try:
        print("--------------------------------------------------------------")
        print("Displaying table contents")
        print("--------------------------------------------------------------")
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql(query, connection_str)
        return df
    
    except Exception as error:
        print("Failed to load table data ❌!", error)

def drop_table(connection_str):

    try:
        print("--------------------------------------------------------------")
        print("Dropping a table in the database")
        print("--------------------------------------------------------------")
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

    try:
        print("--------------------------------------------------------------")
        print("Opening SQL file")
        print("--------------------------------------------------------------")
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
  
    try:
        print("--------------------------------------------------------------")
        print("Exporting table to CSV")
        print("--------------------------------------------------------------")
        df = load_table_data(connection_str, table_name)
        if df is not None:
            df.to_csv(file_name, index=False)
            print(f"Data from {table_name} exported to {file_name} successfully 👍!")
            
    except Exception as error_message:
        print("Failed to export the csv file ❌", error_message)
        
        
def main():

    os.system('cls')
    
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
                  try:
                     connection_str = connection_to_server()
                  except:
                     connection_str = custom_server_connect()
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
