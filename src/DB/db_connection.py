# db_connection.py
import cx_Oracle
from DB_config import db_config

def get_db_connection():
    try:
        connection = cx_Oracle.connect(
            user=db_config['username'],
            password=db_config['password'],
            dsn=db_config['dsn'],
            encoding=db_config['encoding']
        )
        print("Database connection successful")
        return connection
    except cx_Oracle.DatabaseError as e:
        print(f"Database connection failed: {e}")
        return None
