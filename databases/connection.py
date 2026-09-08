import psycopg2
from core.config import settings

_conn:psycopg2.extensions.connection|None=None

def connect():
    global _conn
    if not _conn:
        _conn=psycopg2.connect(
            host=settings.DatabaseHost,
            password=settings.DatabasePassword,
            user=settings.DatabaseUser,
            port=settings.DatabasePort,
            database=settings.DatabaseName
        )
        cur=_conn.cursor()
        cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(30) UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                email  VARCHAR(200) UNIQUE NOT NULL,
                role VARCHAR(100) NOT NULL
                )
            """)
        _conn.commit()
        cur.close()
        print("database connection successfull..")

def disconnect():
    global _conn
    if _conn:
        _conn.close()
        _conn=None
        print("Database disconnected successfully..")
    else:
        print("Database already disconnected!")
