from inventory_services import (
    add_item,
    list_items,
    remove_item,
    update_item,
    decrease_stock,
    increase_stock
)

from authentication import permission_checker

#Initial Main Menu system which only grants access to actions permitted to the current user
def main_menu(user):
    print("=== Welcome to the Inventory System ===")
    while True:
        print("\nChoose an option:")
        print("1) List items")
        print("2) Add item")
        print("3) Update item")
        print("4) Remove item")
        print("5) Increase item stock")
        print("6) Decrease item stock")

        print("0) Exit")

        choice = input("Enter your choice: ").strip()

        #List items
        if choice == "1":
            if not permission_checker(user, "list_items"):
                print("You do not have permission to do this.")
                continue
            print(list_items())

        #Add items
        elif choice == "2":
            #Check permissions
            if not permission_checker(user, "add_item"):
                print("You do not have permission to do this.")
                continue
            #Add item
            sku = input("SKU: ").strip()
            name = input("Name: ").strip()
            unit = input("Unit (default 'each'): ").strip() or "each"
            min_level = input("Min level (default 0): ").strip() or "0"
            stock = input("Current stock (default 0): ").strip() or "0"
            print(add_item(sku, name, unit, min_level, stock))

        #Update items
        elif choice == "3":
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

        #Remove items
        elif choice == "4":
            #Check permissions
            if not permission_checker(user, "remove_item"):
                print("You do not have permission to do this.")
                continue
            #Remove item
            sku = input("SKU to remove: ").strip()
            print(remove_item(sku))

        #Increase stock
        elif choice == "5":
            #Check permissions
            if not permission_checker(user, "increase_stock"):
                print("You do not have permission to do this.")
                continue
            #Increase the stock by desired amount
            sku = input("SKU to increase: ").strip()
            num = input("Number of stock to increase by: ").strip()
            current_stock = input("Current stock (blank = unchanged): ").strip() or 0
            print(increase_stock(sku, num, current_stock))

        #Decrease stock
        elif choice == "6":
            #Check permissions
            if not permission_checker(user, "decrease_stock"):
                print("You do not have permission to do this.")
                continue
            #Decrease the stock by desired amount
            sku = input("SKU to decrease: ").strip()
            num = input("Number of stock to decrease by: ").strip()
            current_stock = input("Current stock (blank = unchanged): ").strip() or 0
            print(decrease_stock(sku, num, current_stock))

        #Exit
        elif choice == "0":
            print("Exiting... Goodbye!")
            break

        #Failsafe
        else:
            print("Invalid choice. Please try again.")

