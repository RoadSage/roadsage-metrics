"""
SQLite database for local development and testing
"""

from piccolo.engine.sqlite import SQLiteEngine

DB = SQLiteEngine("./database.db")


"""
To connect to a PostgreSQL database, use the following: (where DATABASE_URL is the connection URL for the database)
"""

# import os
# from piccolo.engine.postgres import PostgresEngine

# DB = PostgresEngine({"dsn": os.environ["DATABASE_URL"]})
