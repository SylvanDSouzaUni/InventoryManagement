Developed By: Sylvan D'Souza

Overview: This is a simple Inventory Management System (IMS) for Fylde Aero, enabling staff to efficiently record, update, and monitor inventory data. The tool centralises resource management and may reduce errors caused by miscommunication or disorganisation.

How it works:
    Main.py - Entry point
    Menu_options.py - Handles user interface
    Inventory_services.py - Core logic for inventory actions
    Authentication.py - Manages password hashing and overall security logic
    Database_manager.py - Creates and connects to SQLite database securely


Database Tables:
    Users - Stores user credentials and roles
    Items - Stores item data including stock information
    Requests - Stores data regarding requests for items to be added to the company
    Orders - Stores data about orders for more stock, including timestamps to indicate when the order was placed and received.


Starting the program
    Open the project folder in PyCharm or any other Python IDE
    Run the program by executing main.py
    On first launch a default admin account will be created with the following credentials:
      Username: admin
      Password: admin123
    Log in using these credentials
  
  Logging in
    Upon launch you are prompted to log in with your credentials.
    Enter your credentials.
    If successful in logging in, your role will determine which action you can perform
  
  Main Menu Navigation
    After logging in, you will see the main menu.
    Type the number for the desired action and press ENTER
    Follow the on-screen prompts carefully
    Press ENTER when prompted to continue after tables have been listed, or to give confirmation if deleting data.
  
  User Roles and Permissions
    Admin - Full control to any action
    Engineer- Can list items, decrease stock, update items, submit item requests and place orders
    Warehouse - Can list items, increase stock, update items, submit item requests and receive orders
    If you attempt an action which is not permitted for your role, you will receive an error message explaining this.
  
  Admin Actions
    All admin exclusive actions have been bundled into a specific area in the main menu.
    This area can be accessed by entering the number 9 when in the main menu, then pressing enter.
    Here, admins are shown all admin actions which includes user management, order management, request management, add items and remove items.
    Menu navigation here is exactly the same as the main menu.
    You can enter 0 to go back to the main menu.
    NOTE: If you go into “Manage Users”, “Manage Requests”, “Manage Orders”, you will be taken into a separate menu to complete actions which are associated with what you have chosen. You will have the option to go back to the admin menu in these menus too.
  
  User Management
    Within this menu, admins can:
      Create new users
      Delete existing users
      List users
    Enter the number for the action you want to complete, and follow the prompts to complete the action.
  
  Item Actions
  Add item - Adds a new item to the inventory
  Update item - Updates values for fields of that item such as name, stock, etc
  Increase/Decrease stock - Adjust quantities conveniently
  List items - Lists all current items in the inventory in a tabular format
  List Low Stock Items - Lists all items where current stock has reached a critical value
  
  
  Item Request System
    For Engineers/Warehouse
      Navigate to and select submit item request
      Enter the details you desire
      This request is then saved for the admin to view
    For Admins
      Navigate to “Manage Requests” in the admin exclusive menu
        Here you can:
          List Requests - View all pending requests
          Approve Requests - Approve a request which adds the requested item to the items table.
          Reject Request - Permanently delete a request
        When approving a request, 
          All fields can be edited
          You may be prompted to enter mandatory fields such as SKU
  
  Order Management System
    For Engineers/Warehouse
      Navigate to and select Place Order
      Enter the details required
      This request is then saved for the admin to view#
    For warehouse staff
      When stock arrives you can receive the order
      Enter the order ID
        Review details of the order
        Press enter to receive or reply cancel to cancel to abort
      Upon confirmation
        The system updates the stock of the item
        The order status is changed to “RECEIVED”
        A timestamp marks when the order was received
    For Admins
      Navigate to “Manage Orders” to,
        List orders 
        Delete Orders
  
  Logging out and exiting the system
    Select 0 in the main menu to log out, where you will be taken back to the log in screen
    Select * to terminate the program
  
