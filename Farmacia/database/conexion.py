import sqlite3

DB_NAME = "database/farmacia.db"


def get_connection():
    conexion = sqlite3.connect(DB_NAME)
    conexion.row_factory = sqlite3.Row
    return conexion