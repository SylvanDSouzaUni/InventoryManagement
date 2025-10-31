from database_manager import create_schema, get_connection
from authentication import create_starting_admin, login, create_user
from menu_options import main_menu


def main_loop():
    create_schema()
    create_starting_admin()

    while True:
        print("PLEASE LOG IN WITH YOUR CREDENTIALS")
        user = None
        while not user:
            user = login()

        current_status = main_menu(user)

        if current_status == "logged out":
            continue
        elif current_status == "exit":
            break

if __name__ == "__main__":
    main_loop()