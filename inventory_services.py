import sqlite3

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

#============ITEM ACTIONS===================#

#Add item to inventory table
#Available to: ADMIN
def add_item(sku, name, unit, min_level, stock):
    try:
        sku = validation_for_integer_input(sku, "SKU")
        name = validation_for_string_input(name, "NAME")
        unit = validation_for_string_input(unit, "UNIT")
        minimum_stock = validation_for_integer_input(min_level, "MIN_STOCK")
        stock = validation_for_integer_input(stock, "STOCK")

        with get_connection() as connection:
            connection.execute(
                "INSERT INTO items (sku, item_name, unit, min_stock, stock) VALUES (?, ?, ?, ?, ?)",
                (sku, name, unit, minimum_stock, stock)
            )
        return f"Item ({name}) successfully added."

    except sqlite3.IntegrityError:
        return f"[ERROR] SKU must be unique. An item with this sku ({sku}) already exists."

    except Exception as e:
        return f"Failed to add item. [ERROR: {e}]"

#Remove item from inventory table
#Available to: ADMIN
def remove_item(sku):
    try:
        sku = validation_for_integer_input(sku, "SKU")

        with get_connection() as connection:
            item_row = connection.execute("select item_name from items where sku = ?", (sku,)).fetchone()

        if not item_row:
            return f"Item ({sku}) not found."

        item_name = item_row['item_name']

        confirmation = input(f"You are about to remove item ({item_name}) from your inventory. Press ENTER to continue or input CANCEL to cancel: ").strip().lower()

        if confirmation == "cancel":
            return "Successfully cancelled."

        with get_connection() as connection:
            cursor = connection.execute("DELETE FROM items WHERE sku = ?", (sku,))
            if cursor.rowcount > 0:

                return f"{item_name} ({sku}) successfully removed."
            else:
                return f"Item ({sku}) not found."
    except Exception as e:
        return f"Failed to remove item. [ERROR: {e}]"

#Update item in inventory table
#Available to: ADMIN, ENGINEER, WAREHOUSE
def update_item(sku, name = None, unit = None, min_stock = None, stock = None):
    try:
        validation_for_non_empty_input(sku, "SKU")

        update_list = []
        values_for_update_list = []
        errors = []


        #Validate updated value for stock and add it to update list
        if stock is not None:
            try:
                stock = validation_for_integer_input(stock, "STOCK")
                update_list.append("stock = ?")
                values_for_update_list.append(stock)

            except Exception as e:
                errors.append(str(e))

        #Validate updated value for min_stock and add it to update list
        if min_stock is not None:
            try:
                min_stock = validation_for_integer_input(min_stock, "MIN_STOCK")
                update_list.append("min_stock = ?")
                values_for_update_list.append(min_stock)
            except Exception as e:
                errors.append(str(e))

        #Validate updated value for unit and add it to update list
        if unit is not None:
            try:
                unit = validation_for_string_input(unit, "UNIT")
                update_list.append("unit = ?")
                values_for_update_list.append(unit)

            except Exception as e:
                errors.append(str(e))

        #Validate updated value for name and add it to update list
        if name is not None:
            try:
                name = validation_for_string_input(name, "NAME")
                update_list.append("item_name = ?")
                values_for_update_list.append(name)

            except Exception as e:
                errors.append(str(e))


        #Raise cumulative errors
        if errors:
            raise ValueError("; ".join(errors))

        if not update_list:
            return f"No fields to update."

        #Complete update
        values_for_update_list.append(sku)
        update = f"update items set {', '.join(update_list)} where sku = ?"

        with get_connection() as connection:
            cursor = connection.execute(update, values_for_update_list)

        if cursor.rowcount > 0:
            return f"Item ({sku}) successfully updated."
        else:
            return f"Item ({sku}) not found."


    except Exception as \
            e:
        return f"Failed to update item. [ERROR: {e}] \n"

#Update inventory table by reporting a decrease in stock of a certain item
#Available to: ADMIN, ENGINEER
def increase_stock(sku, number):
    try:
        sku = validation_for_integer_input(sku, "SKU")
        number = validation_for_integer_input(number, "NUMBER")

        with get_connection() as connection:
            item = connection.execute(
                "SELECT stock, item_name FROM items WHERE sku = ?", (sku,)
            ).fetchone()

            if not item:
                return f"[ERROR] Item ({sku}) not found."

            current_stock = item["stock"]
            new_stock = current_stock + number

            connection.execute(
                "UPDATE items SET stock = ? WHERE sku = ?", (new_stock, sku)
            )

        return f"Increased stock for '{item['item_name']}' ({sku}) from {current_stock} to {new_stock}."

    except Exception as e:
        return f"Failed to increase stock. [ERROR: {e}] \n"

#Update inventory table by reporting an increase in stock of an item
#Available to: ADMIN, WAREHOUSE
def decrease_stock(sku, number):
    try:
        sku = validation_for_integer_input(sku, "SKU")
        number = validation_for_integer_input(number, "NUMBER")

        with get_connection() as connection:
            item = connection.execute(
                "SELECT stock, item_name FROM items WHERE sku = ?", (sku,)
            ).fetchone()

            if not item:
                return f"[ERROR] No item found with SKU {sku}."

            current_stock = item["stock"]
            new_stock = current_stock - number

            if new_stock < 0:
                return f"[WARNING] Cannot reduce stock below 0. Current stock: {current_stock}."

            connection.execute(
                "UPDATE items SET stock = ? WHERE sku = ?", (new_stock, sku)
            )

        return f"[SUCCESS] Decreased stock for '{item['item_name']}' ({sku}) from {current_stock} to {new_stock}."
    except Exception as e:
        return f"Failed to update item. [ERROR: {e}] \n"

#List items in the inventory table
#Available to: ADMIN, WAREHOUSE, ENGINEER
def list_items():
    try:
        with get_connection() as connection:
            rows = connection.execute(f"select * from items").fetchall()

        if not rows:
            return f"No items found."

        table = ["SKU        | NAME                 | UNIT      | MINIMUM STOCK  | STOCK   |" , "-" * 81]

        for row in rows:
            table.append(f"{row['sku']:<8}   | {row['item_name']:<20} | {row['unit']:<5}     | {row['min_stock']:<3}            | {row['stock']:<5}   |")

        print("\n".join(table))
        input("\n Press ENTER to continue...")


    except Exception as e:
        return f"Failed to list items. [ERROR: {e}]"

#List low stock items
#Available to: ADMIN, WAREHOUSE
def list_low_stock_items():
    try:
        with get_connection() as connection:
            rows = connection.execute(
                "select sku, item_name, unit, min_stock, stock from items where stock < min_stock order by sku asc"
            ).fetchall()

        if not rows:
            return f"No items found: All stock levels are sufficient."

        table = [
            "SKU        | "
            "NAME                 | "
            "UNIT      | "
            "MINIMUM STOCK  | "
            "CURRENT STOCK",
            "-" * 75
        ]

        for row in rows:
            table.append(
                f"{row['sku']:<8}   | "
                f"{row['item_name']:<20} | "
                f"{row['unit']:<8}  | "
                f"{row['min_stock']:<5}          | "
                f"{row['stock']:<5}"
            )

        return "\n".join(table)

    except Exception as e:
        return f"Failed to list low-stock items. [ERROR: {e}]"

#Submit a request for a new item
#Available to: ADMIN, WAREHOUSE, ENGINEER
def submit_item_request(requested_by, item_name = None, sku = None, unit = None, min_stock = None, stock = None):
    try:

        #Basic normalisation as validation will occur in approve request instead
        sku = (str(sku).strip()) if sku is not None else None
        item_name = (str(item_name)).strip() if item_name is not None else None
        unit = (str(unit)).strip() if unit is not None else None

        if min_stock not in (None, ""):
            min_stock = validation_for_integer_input(min_stock, "MIN_STOCK")
        else:
            min_stock = None

        if stock not in (None, ""):
            stock = validation_for_integer_input(stock, "STOCK")
        else:
            stock = None


        #Submit to request table
        with get_connection() as connection:
            connection.execute(
                "INSERT INTO requests (sku, item_name, unit, min_stock, stock, requested_by) VALUES (?, ?, ?, ?, ?, ?)",
                (sku, item_name, unit, min_stock, stock, requested_by)
            )

        return f"Item successfully submitted."
    except Exception as e:
        return f"Failed to submit item. [ERROR: {e}]"

#Place order
#Available to: ADMIN, WAREHOUSE, ENGINEER
def place_order(sku, quantity, ordered_by):
    try:
        sku = validation_for_integer_input(sku, "SKU")
        quantity = validation_for_integer_input(quantity, "QUANTITY")

        if quantity <= 0:
            return "[ERROR] Quantity must be greater than 0."

        with get_connection() as connection:
            item = connection.execute(
                "select item_name from items where sku = ?", (sku,)
            ).fetchone()

            if not item:
                return f"[ERROR] Item not found with sku: {sku}"

            cursor = connection.execute(
                "insert into orders (sku, quantity, ordered_by) values (?, ?, ?)", (sku, quantity, ordered_by)
            )

            order_id = cursor.lastrowid

            return f"SUCCESSFULLY ORDERED: Order ID: #{order_id} Name: '{item['item_name']}' (SKU: {sku}) x{quantity}. Status: Awaiting delivery."

    except Exception as e:
        return f"Failed to place order. [ERROR: {e}]"

#Receive order
#Available to: ADMIN, WAREHOUSE
def receive_order(order_id):
    try:
        order_id = validation_for_integer_input(order_id, "ORDER ID")

        with get_connection() as connection:

            row = connection.execute(
                "SELECT o.order_id, o.sku, o.quantity, o.status, i.item_name, i.stock "
                "FROM orders o LEFT JOIN items i ON o.sku = i.sku "
                "WHERE o.order_id = ?", (order_id,)
            ).fetchone()

            if not row:
                return f"[ERROR] Order not found with order_id: {order_id}"

            if row["status"] != "Awaiting delivery":
                return f"[ERROR] ORDER #{order_id} is already {row['status']}."

            if row["item_name"] is None:
                return f"[ERROR] Item with SKU {row['sku']} does not exist."

            print (f"====ORDER INFO===="
                   f"\n Order: #{order_id} "
                   f"\n Name: {row['item_name']} "
                   f"\n SKU: {row['sku']} "
                   f"\n Quantity of order: {row['quantity']}"
                   )

            confirmation = input("Press ENTER to confirm the arrival of this order, else input CANCEL to cancel: ").strip().lower()

            if confirmation == "cancel":
                return "Successfully cancelled."

            new_stock = int(row["stock"]) + int(row["quantity"])

            connection.execute(
                "update items set stock = ? where sku = ?", (new_stock, row['sku'])
            )

            connection.execute(
                "update orders set status = 'RECEIVED', received_at = current_timestamp where order_id = ?", (order_id,)
            )

            return f"\nOrder #{order_id} successfully received. Stock has been updated from {row['stock']} to {new_stock}."

    except Exception as e:
        return f"Failed to receive order. [ERROR: {e}]"
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------#

#==============ADMIN EXCLUSIVE ACTIONS==============#



#====================USER ACTIONS===================#

#List all users user table
def list_user_information():
    try:
        with get_connection() as connection:
            rows = connection.execute(
                f"SELECT * FROM users order by username asc"
            ).fetchall()

        if not rows:
            return "[ERROR] No users found"

        table = []
        table.append("USERNAME       | ROLE       | PASSWORD HASH")
        table.append("-" * 132)
        for row in rows:
            table.append(f"{row['username']:<14} | {row['role']:<10} | {row['password_hash']}")
        print("\n".join(table))
        input("\nPress ENTER to continue")

    except Exception as e:
        return f"Failed to list users: {e}"

#Create a new user to add to the user table
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
            return f"User successfully created: {str(username).strip().lower()}, ({normalised_role_format})"
        else:
            return f"[ERROR] Failed to create user: Username already exists or invalid role"

    except Exception as e:
        return f"Failed to create user: {e}"

#Delete a user from the user table
def delete_existing_user (username):
    try:
        validation_for_string_input(username, "USERNAME")
        confirmation = input(f"{username} is about to be deleted. Are you sure you want to continue? Reply 'Cancel' to exit or press enter to continue: ")
        if confirmation.strip().lower() == "cancel":
            return f"Action cancelled. {username} has not been deleted."


        deleted_user = delete_user(username)

        if deleted_user:
            return f"User successfully deleted: {str(username).strip().lower()}"
        else:
            return f"[ERROR] Failed to delete user: {str(username).strip().lower()}. No such user exists."

    except Exception as e:
        return f"Failed to delete user: {e}"


#===============ITEM REQUEST ACTIONS================#

def approve_item_request(request_id):

    try:

        #Select and display data of request chosen by ADMIN to approve
        with get_connection() as connection:
            request_row = connection.execute(
                "select request_id, sku, item_name, unit, min_stock, stock from requests where request_id =?", (request_id)
            ).fetchone()

        if not request_row:
            return "[ERROR] No request found"

        sku = request_row["sku"]
        item_name = request_row["item_name"]
        unit = request_row["unit"]
        min_stock = request_row["min_stock"]
        stock = request_row["stock"]

        print("\n=====CHOSEN REQUEST=====")
        print(f"REQUEST ID: {request_id}")
        print(f"SKU: {sku}")
        print(f"NAME: {item_name}")
        print(f"UNIT: {unit}")
        print(f"MIN STOCK: {min_stock}")
        print(f"STOCK: {stock}")


        #Offers ADMIN the choice to edit any fields of request before approving
        choice = input("Edit any fields before approval (Y/N)").strip().lower()

        if choice == "y":

            new_sku = input(f"SKU [{sku or ''}: ")
            if new_sku:
                sku = validation_for_integer_input(new_sku, "SKU")

            new_item_name = input(f"NAME [{item_name or ''}]: ")
            if new_item_name:
                item_name = validation_for_string_input(new_item_name, "NAME")

            new_unit = input(f"UNIT [{unit or ''}]: ")
            if new_unit:
                unit = validation_for_string_input(new_unit, "UNIT")

            new_min_stock = input(f"MIN STOCK [{'' if min_stock is None else min_stock}]: ")
            if new_min_stock:
                min_stock = validation_for_integer_input(new_min_stock, "MIN STOCK")

            new_stock = input(f"STOCK [{'' if stock is None else stock}]: ")
            if new_stock:
                stock = validation_for_integer_input(new_stock, "STOCK")


        #Ensures Default values are set for fields that require it
        sku = validation_for_integer_input(sku or input("SKU (required): "), "SKU")
        item_name = validation_for_string_input(item_name or input("NAME (required): "), "NAME")
        stock = validation_for_integer_input(stock or input("STOCK (required, integer): "), "STOCK")

        unit = validation_for_string_input(unit or "each", "UNIT")
        min_stock = validation_for_integer_input(min_stock or 0, "MIN_STOCK")


        #Approve request (add item from request to item table) and delete request from request table
        try:
            with get_connection() as connection:
                connection.execute(
                    "insert into items (sku, item_name, unit, min_stock, stock) values (?, ?, ?, ?, ?)",
                    (sku, item_name, unit, min_stock, stock)
                )
                connection.execute("delete from requests where request_id = ?", (request_id,))
                return f"Request approved. Item [{sku}] has been approved."



        except sqlite3.IntegrityError:
            return "[ERROR] SKU must be unique - An item with this SKU already exists"
        except Exception as e:
            return f"Failed to approve item: [ERROR]: {e}"

    except Exception as e:
        return f"Failed to process approval: [ERROR]: {e}"

def reject_item_request(request_id):
    try:

        confirmation = input(f"You are about to reject a request (Request ID: {request_id}). Press ENTER to continue or reply CANCEL to cancel: ").strip().lower()

        if confirmation == "cancel":
            return f"[CANCEL] Rejection has been cancelled."

        with get_connection() as connection:
            cursor = connection.execute(
                "delete from requests where request_id = ?", (request_id,)
            )

        if cursor.rowcount > 0:
            return f"[CANCEL] Request has been rejected."
        else:
            return f"[ERROR] Request does not exist."

    except Exception as e:
        return f"Failed to reject request: [ERROR]: {e}"

def list_requests():
    try:
        with get_connection() as connection:
            rows = connection.execute(
                "select request_id, sku, item_name, unit, min_stock, stock, requested_by from requests order by request_id"
            ).fetchall()

            if not rows:
                return "[ERROR] No requests found."

            lines = [
                "REQ_ID | "
                "SKU           | "
                "NAME                 | "
                "UNIT  | "
                "MIN | "
                "STOCK | "
                "BY         |",
                "-" * 90
            ]
            for row in rows:
                lines.append(f"{row['request_id']:6} | "
                             f"{str(row['sku'] or ''):<13} | "
                             f"{str(row['item_name'] or ''):<20} | "
                             f"{str(row['unit'] or ''):<5} | "
                             f"{str(row['min_stock'] if row['min_stock'] is not None else ''):<3} | "
                             f"{str(row['stock'] if row['stock'] is not None else ''):<5} | "
                             f"{row['requested_by']:<10} | "
                             )

            return "\n".join(lines)

    except Exception as e:
        return f"Failed to list requests: [ERROR]: {e}"


#==================ORDER ACTIONS====================#

def list_orders():
    try:
        with get_connection() as connection:
            rows = connection.execute(
                "select order_id, sku, quantity, ordered_by, status, ordered_at, received_at from orders order by order_id desc"
            ).fetchall()

        if not rows:
            return "[ERROR] No orders."

        lines = [
            "ID  | "
            "SKU        | "
            "QTY | "
            "BY         | "
            "STATUS             | "
            "ORDERED_AT           | "
            "RECEIVED_AT",
            "-" * 95
        ]

        for row in rows:
            lines.append(
                f"{row['order_id']:3} | "
                f"{str(row['sku']):<10} | "
                f"{row['quantity']:3} | "
                f"{row['ordered_by']:<10} | "
                f"{row['status']:<18} | "
                f"{row['ordered_at']:<19}  | "
                f"{str(row['received_at'] or '')}"
            )

        return "\n".join(lines)

    except Exception as e:
        return f"Failed to list orders: [ERROR]: {e}"

def delete_order(order_id):
    try:
        order_id = validation_for_integer_input(order_id, "ORDER_ID")

        with get_connection() as connection:
            row = connection.execute(
                "SELECT order_id, sku, quantity, ordered_by, status, ordered_at, received_at "
                "FROM orders WHERE order_id = ?",
                (order_id,)
            ).fetchone()

        if not row:
            return f"[INFO] No such order (#{order_id})."

        # Show the order details
        print("\n--- ORDER DETAILS ---")
        print(f"ID:         {row['order_id']}")
        print(f"SKU:        {row['sku']}")
        print(f"Quantity:   {row['quantity']}")
        print(f"Ordered by: {row['ordered_by']}")
        print(f"Status:     {row['status']}")
        print(f"Ordered at: {row['ordered_at']}")
        print(f"Received at:{row['received_at'] if row['received_at'] else ''}")

        confirm = input("\nPress ENTER to delete this order, or type 'cancel' to cancel: ").strip().lower()
        if confirm == "cancel":
            return "Deletion successfully cancelled."

        with get_connection() as connection:
            cur = connection.execute(
                "DELETE FROM orders WHERE order_id = ?",
                (order_id,)
            )

            if cur.rowcount and cur.rowcount > 0:
                return f"Order #{order_id} successfully deleted."
            else:
                return f"There was an error in deleting this order. It may not exist"

    except Exception as e:
        return f"[ERROR] Failed to delete order: {e}"