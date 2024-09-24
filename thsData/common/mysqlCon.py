import pymysql
from pymysql.cursors import DictCursor
from common.config import MYSQL_CONFIG


class MySQLConnector:
    def __init__(self, config=MYSQL_CONFIG):
        self.config = config
        self.connection = None
    def connect(self):
        try:
            self.connection = pymysql.connect(
                **self.config,
                cursorclass=DictCursor
            )
            print("Successfully connected to the database.")
        except pymysql.Error as e:
            print(f"Error connecting to the database: {e}")
            raise

    def execute_query(self, query, params=None):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params or ())
                result = cursor.fetchall()
            self.connection.commit()
            return result
        except pymysql.Error as e:
            print(f"Error executing query: {e}")
            self.connection.rollback()
            raise

    def close(self):
        if self.connection:
            self.connection.close()
            print("Database connection closed.")

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
