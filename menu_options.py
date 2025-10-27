from inventory_services import (
    add_item,
    list_items,
    remove_item,
    update_item,
    decrease_stock,
    increase_stock,
    create_new_user,
    delete_existing_user,
    list_user_information
)

from authentication import permission_checker

#Initial Main Menu system which only grants access to actions permitted to the current user
def main_menu(user):
    print("=== Welcome to the Inventory System ===")
    while True:
        print("\nChoose an option:")
        print("1) List items")
        print("2) Update item")
        print("3) Increase item stock")
        print("4) Decrease item stock")

        print("9) Admin actions")
        print("0) Log out")
        print("*) Exit")

        choice = input("Enter your choice: ").strip()

        #List items
        if choice == "1":
            if not permission_checker(user, "list_items"):
                print("You do not have permission to do this.")
                continue
            print(list_items())

        #Update items
        elif choice == "2":
            #Check permissions
            if not permission_checker(user, "update_item"):
                print("You do not have permission to do this.")
                continue
            # Update item
            sku = input("SKU to update: ").strip()
            new_name = input("New name (blank = unchanged): ").strip() or None
            new_unit = input("New unit (blank = unchanged): ").strip() or None
            new_min = input("New min level (blank = unchanged): ").strip() or None
            new_stock = input("New stock (blank = unchanged): ").strip() or None
            print(update_item(sku, new_name, new_unit, new_min, new_stock))

        #Increase stock
        elif choice == "3":
            #Check permissions
            if not permission_checker(user, "increase_stock"):
                print("You do not have permission to do this.")
                continue
            #Increase the stock by desired amount
            sku = input("SKU to increase: ").strip()
            num = input("Number of stock to increase by: ").strip()
            current_stock = input("Current stock (blank = unchanged): ").strip()
            print(increase_stock(sku, num, current_stock))

        #Decrease stock
        elif choice == "4":
            #Check permissions
            if not permission_checker(user, "decrease_stock"):
                print("You do not have permission to do this.")
                continue
            #Decrease the stock by desired amount
            sku = input("SKU to decrease: ").strip()
            num = input("Number of stock to decrease by: ").strip()
            current_stock = input("Current stock (blank = unchanged): ").strip()
            print(decrease_stock(sku, num, current_stock))

        #Admin exclusive actions
        elif choice == "9":
            #Check permissions
            if not permission_checker(user, "admin_actions"):
                print("You do not have permission to do this.")
                continue
            #Run Admin menu
            admin_exclusive_menu()

        #Log out
        elif choice == "0":
            print("Logging out...")
            return "logged out"

        #Exit
        elif choice == "*":
            print("Exiting..")
            return "exit"

        #Failsafe
        else:
            print("Invalid choice. Please pick the number corresponding to your desired action.")

#Seperate menu system for admin exclusive actions
def admin_exclusive_menu():
    while True:
        print("\n=====ADMIN MANAGEMENT=====")
        print("1) Manage users")
        print("2) Add item")
        print("3) Remove item")

        print("0) Back")

        choice = input("Enter your choice: ").strip()

        #Manage users
        if choice == "1":
            user_management_menu()

        #Add items
        elif choice == "2":
            # Add item
            sku = input("SKU: ").strip()
            name = input("Name: ").strip()
            unit = input("Unit (default 'each'): ").strip() or "each"
            min_level = input("Min level (default 0): ").strip() or "0"
            stock = input("Current stock (default 0): ").strip() or "0"
            print(add_item(sku, name, unit, min_level, stock))

        #Remove items
        elif choice == "3":
            # Remove item
            sku = input("SKU to remove: ").strip()
            print(remove_item(sku))

        #Back
        elif choice == "0":
            print("\nReturning to Main Menu...")
            return

        # Failsafe
        else:
            print("Invalid choice. Please pick the number corresponding to your desired action.")

#Seperate menu system for admin to handle users
def user_management_menu():
    while True:
        print("\n=====MANAGE USERS=====")
        print("1) Create user")
        print("2) Delete user")
        print("3) List user information")
        print("0) Back ")
        choice = input("Enter your choice: ").strip()

        #Add user to table
        if choice == "1":
            username = input("Username to add: ").strip()
            password = input("Password of new account: ").strip()
            role = input("Role of new account: ").strip()
            print(create_new_user(username, password, role))

        #Remove user from table
        elif choice == "2":
            username = input("Username to delete: ").strip()
            print(delete_existing_user(username))

        #List user info
        elif choice == "3":
            #List all user info
            list_user_information()

        #Back
        elif choice == "0":
            print("\nReturning to Admin Menu...")
            return

        #Failsafe
        else:
            print("Invalid choice. Please pick the number corresponding to your desired action.")
