from authentication import (create_user, delete_user)
from database_manager import get_connection

#_______VALIDATION______#

#Reusable function to validate integer inputs
def validation_for_integer_input(value, field):
    try:
        integer = int(value)
        stripped_integer = str(integer).strip()
    except Exception:
        raise ValueError(f"{field} must be an integer")
    if integer < 0:
        raise ValueError(f"{field} must be positive")
    if not stripped_integer:
        return ValueError(f"{field} must not be empty")
    return integer

#Reusable function to validate non-empty inputs
def validation_for_non_empty_input(value, field):
    stripped_value = str(value).strip()
    if not stripped_value:
        raise ValueError(f"'{field}' must not be empty")

#Reusable function to validate string inputs
def validation_for_string_input(value, field):
    stripped_value = str(value).strip()
    if not stripped_value:
        raise ValueError(f"'{field}' must not be empty")
    if stripped_value.isdigit():
        raise ValueError(f"'{field}' must not be an integer")
    return value

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------#


#Add item to inventory table
#Available to: ADMIN
def add_item(sku, name, unit, min_level, stock):
    try:
        validation_for_non_empty_input(sku, "SKU")
        validation_for_non_empty_input(name, "NAME")
        minimum_stock = validation_for_integer_input(min_level, "MIN_STOCK")
        return f"Item successfully added. SKU: {sku}, NAME: {name}, MIN_STOCK: {minimum_stock}, UNIT: {unit}, STOCK: {stock}"
    except Exception as e:
        return f"Failed to add item. [ERROR: {e}] \n"

#Remove item from inventory table
#Available to: ADMIN
def remove_item(sku):
    try:
        validation_for_non_empty_input(sku, "SKU")
        return f"Item successfully removed. SKU: {sku}"
    except Exception as e:
        return f'Failed to remove item. [ERROR: {e}] \n'

#List all users user table
#Available to: ADMIN
def list_user_information():
    try:
        with get_connection() as connection:
            rows = connection.execute(
                f"SELECT * FROM users ORDER BY id"
            ).fetchall()

        if not rows:
            return "[ERROR] No users found"

        table = []
        table.append("ID | USERNAME       | ROLE       | PASSWORD HASH")
        table.append("-" * 132)
        for row in rows:
            table.append(f"{row['id']:2} | {row['username']:<14} | {row['role']:<10} | {row['password_hash']}")
        print("\n".join(table))
        input("\nPress ENTER to continue")

    except Exception as e:
        return f"Failed to list users: {e}"

#Create a new user to add to the user table
#Available to: Admin
def create_new_user(username, password, role):
    try:
        validation_for_string_input(username, "USERNAME")
        validation_for_string_input(password, "PASSWORD")
        validation_for_string_input(role, "ROLE")

        normalised_role_format = str(role).strip().title()

        if normalised_role_format not in ('Admin', 'Engineer', 'Warehouse'):
            return "[ERROR] You have provided an invalid role. Please choose from: Admin, Engineer, Warehouse"

        created_user = create_user(username, password, normalised_role_format)

        if created_user:
            return f"[SUCCESS] User successfully created: {str(username).strip().lower()}, ({normalised_role_format})"
        else:
            return f"[ERROR] Failed to create user: Username already exists or invalid role"

    except Exception as e:
        return f"Failed to create user: {e}"

#Delete a user from the user table
#Available to: Admin
def delete_existing_user (username):
    try:
        validation_for_string_input(username, "USERNAME")
        confirmation = input(f"{username} is about to be deleted. Are you sure you want to continue? Reply 'Cancel' to exit or press enter to continue: ")
        if confirmation.strip().lower() == "cancel":
            print (f"Action cancelled. {username} has not been deleted.")
            return

        deleted_user = delete_user(username)
        if deleted_user:
            return f"[SUCCESS] User successfully deleted: {str(username).strip().lower()}"
        else:
            return f"[ERROR] Failed to delete user: {str(username).strip().lower()}. No such user exists."

    except Exception as e:
        return f"Failed to delete user: {e}"

#Update inventory table by reporting a decrease in stock of a certain item
#Available to: ADMIN, ENGINEER
def decrease_stock(sku, number, current_stock):
    try:
        validation_for_non_empty_input(sku, "SKU")
        validation_for_integer_input(number, "NUMBER")
        validation_for_integer_input(current_stock, "CURRENT_STOCK")
        return f"Item successfully updated. SKU: {sku}, NEW STOCK NUMBER: {int(current_stock) - int(number)}"
    except Exception as e:
        return f"Failed to update item. [ERROR: {e}] \n"

#Update inventory table by reporting an increase in stock of an item
#Available to: ADMIN, WAREHOUSE
def increase_stock(sku, number, current_stock):
    try:
        validation_for_non_empty_input(sku, "SKU")
        validation_for_integer_input(number, "NUMBER")
        validation_for_integer_input(current_stock, "CURRENT_STOCK")
        return f"Item successfully updated. SKU: {sku}, NEW STOCK NUMBER: {int(current_stock) + int(number)}"
    except Exception as e:
        return f"Failed to update item. [ERROR: {e}] \n"

#List items in the inventory table
#Available to: ADMIN, WAREHOUSE, ENGINEER
def list_items():
    return "Inventory currently empty"

#Update item in inventory table
#Available to: ADMIN, ENGINEER, WAREHOUSE
def update_item(sku, name = None, unit = None, min_stock = None, stock = None):
    errors = []
    try:
        validation_for_non_empty_input(sku, "SKU")

        if stock is not None:
            try:
                stock = validation_for_integer_input(stock, "STOCK")
            except Exception as e:
                errors.append(str(e))

        if min_stock is not None:
            try:
                min_stock = validation_for_integer_input(min_stock, "MIN_STOCK")
            except Exception as e:
                errors.append(str(e))

        if unit is not None:
            try:
                unit = validation_for_integer_input(unit, "UNIT")
            except Exception as e:
                errors.append(str(e))

        if name is not None:
            try:
                name = validation_for_string_input(name, "NAME")
            except Exception as e:
                errors.append(str(e))

        if errors:
            raise ValueError("; ".join(errors))

        return (f" Item successfully updated."
                f" SKU: {sku}"
                f" Name={name or '[UNCHANGED]'}"
                f" Unit={unit or '[UNCHANGED]'}"
                f" Minimum stock={min_stock or '[UNCHANGED]'}"
                f" Stock={stock or '[UNCHANGED]'}"
                )
    except Exception as e:
        return f"Failed to update item. [ERROR: {e}] \n"





