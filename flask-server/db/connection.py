import psycopg2
import os

def get_db_connection():
    conn = psycopg2.connect(
        host='localhost',
        database='Clothing',
        user='postgres',
        password='42gpAduw'
    )
    return conn