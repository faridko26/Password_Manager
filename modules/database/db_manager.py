import mysql.connector
from getpass4 import getpass


class DatabaseManager:
    def __init__(self, host="localhost", user="root", password=None):
        self.host = host
        self.user = user
        self.password = password
        self.connection = None
        self.cursor = None

    def connect(self):
        if not self.password:
            self.password = getpass("Enter your password: ")
        self.connection = mysql.connector.connect(
            host=self.host, user=self.user, password=self.password
        )
        self.cursor = self.connection.cursor()

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

        # print(f"Schema '{schema_name}' created")

    def create_table(self, schema_name, table_name):
        query = f"""CREATE TABLE {schema_name}.{table_name} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        website VARCHAR(255) NOT NULL,
        username VARCHAR(100),
        password VARCHAR(255) NOT NULL,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )"""
        self.cursor.execute(query)
        print(f"Table '{table_name}' created in schema '{schema_name}'")

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def execute(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()
