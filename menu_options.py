from inventory_services import (
    add_item,
    list_items,
    remove_item,
    update_item,

    decrease_stock,
    increase_stock,

    create_new_user,
    delete_existing_user,
    list_user_information,

    submit_item_request,
    approve_item_request,
    reject_item_request,
    list_requests,

    list_low_stock_items,

    place_order,
    receive_order,
    list_orders,
    delete_order,

)

from authentication import permission_checker

#Initial Main Menu system which only grants access to actions permitted to the current user
def main_menu(user):
    print("=== Welcome to the Inventory System ===")
    while True:
        print("\n=====MAIN MENU=====")
        print("Choose an option:")
        print("1) List items")
        print("2) Update item")
        print("3) Increase item stock")
        print("4) Decrease item stock")
        print("5) Submit item request")
        print("6) View Low Stock items")
        print("7) Place Order")
        print("8) Receive Order")


        print("9) Admin actions")
        print("0) Log out")
        print("*) Exit")

        choice = input("Enter your choice: ").strip()

        #List items
        if choice == "1":
            if not permission_checker(user, "list_items"):
                print("You do not have permission to do this.")
                continue
            list_items()

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
            print(increase_stock(sku, num))

        #Decrease stock
        elif choice == "4":
            #Check permissions
            if not permission_checker(user, "decrease_stock"):
                print("You do not have permission to do this.")
                continue
            #Decrease the stock by desired amount
            sku = input("SKU to decrease: ").strip()
            num = input("Number of stock to decrease by: ").strip()
            print(decrease_stock(sku, num))

        #Submit Item Request
        elif choice == "5":
            #Check permissions
            if not permission_checker(user, "submit_item_request"):
                print("You do not have permission to do this.")
                continue
            #Submit Item request
            sku = input("SKU to list: ").strip()
            name = input("Name: ").strip() or None
            unit = input("Unit: ").strip() or None
            stock = input("Stock: ").strip() or None
            min_stock = input("Minimum Stock: ").strip() or None
            requested_by = user["username"]

            print(submit_item_request(requested_by, name, sku, unit, min_stock, stock))

        #Check low stock items
        elif choice == "6":
            #Check permissions
            if not permission_checker(user, "list_low_stock_items"):
                print("You do not have permission to do this.")
                continue
            #Return list of low stock items
            print(list_low_stock_items())
            input("\nPress ENTER to continue...")

        #Place order
        elif choice == "7":
            #Check permissions
            if not permission_checker(user, "place_order"):
                print("You do not have permission to do this.")
                continue

            #Place order
            sku = input("SKU of item being ordered: ").strip()
            quantity = input("Quantity of stock being ordered: ").strip() or None
            ordered_by = user["username"]
            print(place_order(sku, quantity, ordered_by))

        #Receive order
        elif choice == "8":
            #Check permissions
            if not permission_checker(user, "receive_order"):
                print("You do not have permission to do this.")
                continue

            #Receive order
            order_id = input("Order ID: ").strip()
            print(receive_order(order_id))

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

        print("1) Add item")
        print("2) Remove item")
        print("3) Manage users")
        print("4) Manage requests")
        print("5) Manage orders")

        print("0) Back")

        choice = input("Enter your choice: ").strip()


        #Add items
        if choice == "1":
            # Add item
            sku = input("SKU: ").strip()
            name = input("Name: ").strip()
            unit = input("Unit (default 'each'): ").strip() or "each"
            min_level = input("Min level (default 0): ").strip() or "0"
            stock = input("Current stock (default 0): ").strip() or "0"
            print(add_item(sku, name, unit, min_level, stock))

        #Remove items
        elif choice == "2":
            # Remove item
            sku = input("SKU to remove: ").strip()
            print(remove_item(sku))

        #Manage users
        elif choice == "3":
            user_management_menu()

        #Manage Requests
        elif choice == "4":
            request_management_menu()

        #Manage orders
        elif choice == "5":
            order_management_menu()

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

#Seperate menu system for admin to handle requests
def request_management_menu():
    while True:
        print("\n=====MANAGE REQUESTS=====")
        print("1) Approve request")
        print("2) Reject request")
        print("3) List requests")

        print("0) Back ")
        choice = input("Enter your choice: ").strip()

        #Add user to table
        if choice == "1":
            id = input("Request ID of request to approve: ").strip()
            print(approve_item_request(id))

        #Remove user from table
        elif choice == "2":
            id = input("Request ID of request to reject: ").strip()
            print(reject_item_request(id))

        #List user info
        elif choice == "3":
            #List all user info
            print(list_requests())
            input("\n Press ENTER to continue...")

        #Back
        elif choice == "0":
            print("\nReturning to Admin Menu...")
            return

        #Failsafe
        else:
            print("Invalid choice. Please pick the number corresponding to your desired action.")

#Seperate menu system to manage orders
def order_management_menu():
    while True:
        print("\n=====MANAGE REQUESTS=====")
        print("1) List orders")
        print("2) Delete order")

        print("0) Back ")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            print(list_orders())
            input("\n Press ENTER to continue...")

        elif choice == "2":
            order_id = input("Order ID of order to delete: ").strip()
            delete_order(order_id)

        elif choice == "0":
            print("\nReturning to Admin Menu...")
            return

        # Failsafe
        else:
            print("Invalid choice. Please pick the number corresponding to your desired action.")