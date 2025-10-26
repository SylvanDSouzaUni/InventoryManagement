import hashlib, secrets
from database_manager import get_connection

#Available roles
ROLES = ('Admin', 'Engineer', 'Warehouse')

#Structure to store actions that each role is permitted to do
PERMISSIONS = {
    'Admin':     {'list_items', 'add_item', 'update_item', 'remove_item', 'decrease_stock', 'increase_stock'},
    'Engineer':  {'list_items', 'update_item', 'decrease_stock'},
    'Warehouse': {'list_items', 'update_item', 'increase_stock'},
}

#Function to hash passwords
def hash_password(password):
    """Return 'salt$hash' using SHA-256."""
    salt = secrets.token_hex(16)
    hashable_input = salt+password
    hash_result = hashlib.sha256(hashable_input.encode()).hexdigest()
    return f"{salt}${hash_result}"

#Function to verify passwords on login attempts
def check_password(password_attempt, stored):
    try:
        salt, stored_hash = stored.split("$", 1)
    except ValueError:
        return False
    test = hashlib.sha256((salt + password_attempt).encode()).hexdigest()

    if test == stored_hash:
        return True
    else:
        return False

#Function to create a user and add it to user table in database
def create_user(username, password, role):
    hashed_password = hash_password(password)
    with get_connection() as connection:
        connection.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (?,?,?)", (username.strip(), hashed_password, role)
        )

#Funciton to create a starting account if no accounts exist already. This account will be admin.
def create_starting_admin():
    with get_connection() as connection:
        row = connection.execute("SELECT COUNT(*) AS count FROM users").fetchone()
    if row["count"] == 0:
        create_user("admin", "admin123", "Admin")
        print("[INFO] Created default admin account: admin / admin123")

#Login functionality
def login():
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    with get_connection() as conn:
        row = conn.execute(
            "SELECT id, username, password_hash, role FROM users WHERE username=?",
            (username,)
        ).fetchone()
    if not row:
        print("User not found.")
        return None
    if not check_password(password, row["password_hash"]):
        print("Incorrect password.")
        return None
    return {"id": row["id"], "username": row["username"], "role": row["role"]}

#Function to check if a user is allowed to complete a certain action.
def permission_checker(user, action):
    if action in PERMISSIONS.get(user["role"], set()):
        return True
    else:
        return False
