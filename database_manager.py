import sqlite3
from pathlib import Path

#Function to define path to inventory database
database_path = Path(__file__).with_name("inventory_manager.db")

#Reusable function to return a connection to the database
def get_connection():
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON;")
    return connection


#Function to define structure of database
def create_schema():
    with get_connection() as connection:
        connection.executescript("""
            create table if not exists users (
            id integer primary key autoincrement,
            username text not null unique,
            password_hash text not null,
            role text not null check (role IN ('Admin', 'Engineer', 'Warehouse'))
                );
        """)


