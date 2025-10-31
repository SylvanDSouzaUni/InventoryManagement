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
            username text not null unique,
            password_hash text not null,
            role text not null check (role IN ('Admin', 'Engineer', 'Warehouse'))
                );
                
            create table if not exists items (
                sku text not null unique,
                item_name text not null,
                unit text not null default 'each',
                min_stock integer not null default 0,
                stock integer not null default 0
            );
                
            create table if not exists requests (
                request_id integer primary key autoincrement,
                sku text,
                item_name text,
                unit text default 'each',
                min_stock integer default 0,
                stock integer default 0,
                requested_by text not null 
            );
                
        """)


