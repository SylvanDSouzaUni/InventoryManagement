from database_manager import create_schema
from authentication import create_starting_admin, login, create_user
from menu_options import main_menu

def main_loop():
    create_schema()
    create_starting_admin()
    print("PLEASE LOG IN WITH YOUR CREDENTIALS")
    user = None
    while not user:
        user = login()
    main_menu(user)

if __name__ == "__main__":
    main_loop()