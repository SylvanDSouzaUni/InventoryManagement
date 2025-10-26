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

#Reusable function to validate inputs that must have a value
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
        raise ValueError(f"'{field}' must not be empty")
    return value

#Function to add item to inventory
def add_item(sku, name, unit, min_level, stock):
    try:
        validation_for_non_empty_input(sku, "SKU")
        validation_for_non_empty_input(name, "NAME")
        minimum_stock = validation_for_integer_input(min_level, "MIN_STOCK")
        return f"Item successfully added. SKU: {sku}, NAME: {name}, MIN_STOCK: {minimum_stock}, UNIT: {unit}, STOCK: {stock}"
    except Exception as e:
        return f"Failed to add item. [ERROR: {e}] \n"


#Function to list inventory
def list_items():
    return "Inventory currently empty"

#Function to remove item from inventory
def remove_item(sku):
    try:
        validation_for_non_empty_input(sku, "SKU")
        return f"Item successfully removed. SKU: {sku}"
    except Exception as e:
        return f'Failed to remove item. [ERROR: {e}] \n'


#Function to update item in inventory
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

        return (f" Item successfuly updated."
                f" SKU: {sku}"
                f" Name={name or '[UNCHANGED]'}"
                f" Unit={unit or '[UNCHANGED]'}"
                f" Minimum stock={min_stock or '[UNCHANGED]'}"
                f" Stock={stock or '[UNCHANGED]'}"
                )
    except Exception as e:
        return f"Failed to update item. [ERROR: {e}] \n"



