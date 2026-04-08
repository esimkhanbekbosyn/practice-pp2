import psycopg2
from config import host, database, user, password, port


def get_connection():
    return psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password,
        port=port
    )