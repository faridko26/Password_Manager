import mysql.connector
from getpass4 import getpass
import sys


class DatabaseManager:
    def __init__(self, host="localhost", user="root", password=None):
        self.host = host
        self.user = user
        self.password = password
        self.connection = None
        self.cursor = None

    def connect(self):
        attempts = 0
        while attempts < 3:  # Limit to 3 attempts
            try:
                self.user = input("Enter your username: ")
                self.password = getpass("Enter your password: ")
                self.connection = mysql.connector.connect(
                    host=self.host, user=self.user, password=self.password
                )
                self.cursor = self.connection.cursor()
                return (
                    self.connection,
                    self.cursor,
                )  # Successful connection, return connection and cursor
            except mysql.connector.Error as e:
                attempts += 1
                print("Error connecting to the database:", e.msg)
                if attempts < 3:
                    print(f"Please try again. {3 - attempts} attempts remaining.")
                else:
                    print("Maximum attempts reached. Exiting.")
                    sys.exit()  # Exit the program if maximum attempts reached

        return (
            None,
            None,
        )  # Return None for connection and cursor if maximum attempts reached

    def check_schema_exists(self, schema_name):
        self.cursor.execute("SHOW DATABASES")
        for db in self.cursor.fetchall():
            if schema_name in db[0]:
                # print(f"Schema '{schema_name}' exists")
                return True
        return False

    def check_table_exists(self, schema_name, table_name):
        if not self.check_schema_exists(schema_name):
            return False
        self.cursor.execute(f"SHOW TABLES IN {schema_name}")
        for table in self.cursor.fetchall():
            if table_name in table[0]:
                # print(f"Table '{table_name}' exists in schema '{schema_name}'")
                return True
        return False

    def setup_db(self, schema_name="pwd_manager", table_name="accounts"):
        if not self.check_schema_exists(schema_name):
            self.cursor.execute(f"CREATE SCHEMA {schema_name}")
            self.create_table(schema_name, table_name)

        if self.check_schema_exists(schema_name):
            if not self.check_table_exists(schema_name, table_name):
                self.create_table(schema_name, table_name)
        self.cursor.execute(f"USE {schema_name}")
        # print(f"Schema '{schema_name}' created")

    def create_table(self, schema_name, table_name):
        query = f"""CREATE TABLE {schema_name}.{table_name} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        website VARCHAR(255) NOT NULL,
        username VARCHAR(100),
        password BLOB NOT NULL,
        salt BINARY(16) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )"""
        self.cursor.execute(query)
        # print(f"Table '{table_name}' created in schema '{schema_name}'")

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def execute_query(self, query, params=None, schema_name="pwd_manager"):
        # self.cursor.execute(f"USE {schema_name}")
        self.cursor.execute(query, params)
        self.connection.commit()

    def delete_db(self, schema_name="pwd_manager"):
        while True:
            choice = (
                input(
                    f"Are you sure you want to delete the database '{schema_name}'? (y/n):"
                )
                .strip()
                .lower()
            )
            if choice in ["y", "n"]:
                break
            else:
                print("Invalid input. Please enter 'y' or 'n'.")

        if choice == "y":
            if self.check_schema_exists(schema_name):
                self.cursor.execute(f"DROP SCHEMA {schema_name}")
                print("\n" + "-" * 40)
                print(f" Database '{schema_name}' deleted successfully!")
                print("-" * 40 + "\n")
            else:
                print("\n" + "-" * 40)
                print(f"Database '{schema_name}' does not exist.")
                print("-" * 40 + "\n")

        else:
            print("\n" + "-" * 40)
            print("Database deletion canceled.")
            print("-" * 40 + "\n")

    def fetch_all(self, query, params=None):
        if self.check_schema_exists(schema_name="pwd_manager"):
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        else:
            return None

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()
