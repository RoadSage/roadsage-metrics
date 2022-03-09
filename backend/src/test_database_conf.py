"""
Database Configuration for Unit Tests

If you are trying to deploy the application, you likely want to change database_conf.py instead. This file is only used in Unit Tests.
"""


from piccolo.engine.sqlite import SQLiteEngine

DB = SQLiteEngine("./test.db")
