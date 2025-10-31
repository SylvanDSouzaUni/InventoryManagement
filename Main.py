from database_manager import create_schema, get_connection
from authentication import create_starting_admin, login, create_user
from menu_options import main_menu

with get_connection() as conn:
    conn.executescript("""
        DROP TABLE IF EXISTS users;
        DROP TABLE IF EXISTS items;
        DROP TABLE IF EXISTS requests;
    """)

create_schema()
print("✅ Tables deleted and recreated.")

def main_loop():
    create_schema()
    create_starting_admin()

    while True:
        print("PLEASE LOG IN WITH YOUR CREDENTIALS")
        user = None
        while not user:
            user = login()
        print(user)
        current_status = main_menu(user)

        if current_status == "logged out":
            continue
        elif current_status == "exit":
            break

if __name__ == "__main__":
    main_loop()