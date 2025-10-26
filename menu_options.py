# menu_options.py — simple console menu wired to inventory_services (with stock prompts)
from inventory_services import (
    add_item,
    list_items,
    remove_item,
    update_item,
)

def main_menu():
    print("=== Welcome to the Inventory System ===")
    while True:
        print("\nChoose an option:")
        print("1) List items")
        print("2) Add item")
        print("3) Update item")
        print("4) Remove item")
        print("0) Exit")

        choice = input("Enter your choice: ").strip()

        #Print all items in inventory
        if choice == "1":
            print(list_items())

        #Add item 
        elif choice == "2":
            sku = input("SKU: ").strip()
            name = input("Name: ").strip()
            unit = input("Unit (default 'each'): ").strip() or "each"
            min_level = input("Min level (default 0): ").strip() or "0"
            stock = input("Current stock (default 0): ").strip() or "0"
            print(add_item(sku, name, unit, min_level, stock))

        #Update item (all fields optional except SKU)
        elif choice == "3":
            sku = input("SKU to update: ").strip()
            new_name = input("New name (blank = unchanged): ").strip() or None
            new_unit = input("New unit (blank = unchanged): ").strip() or None
            new_min = input("New min level (blank = unchanged): ").strip() or None
            new_stock = input("New stock (blank = unchanged): ").strip() or None
            print(update_item(sku, new_name, new_unit, new_min, new_stock))

        #Remove items
        elif choice == "4":
            sku = input("SKU to remove: ").strip()
            print(remove_item(sku))

        #Exit code
        elif choice == "0":
            print("Exiting... Goodbye!")
            break

        #Failsafe
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
