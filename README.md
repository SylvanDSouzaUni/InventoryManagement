Version 1.4

This version marks the end of the project.
In this version, order functionality was added.
Warehouse and Engineers can place orders for items by specifying item sku.
These orders can be viewed by admin, who has the ability to delete them.
Once an order arrives, warehouse are able to notify the program through the receive_order function. This function will automatically increase the stock of this item in the item table. 
Orders are timestamped with order time and order received time. Orders can exist in one of two states: AWAITING DELIVERY, RECEIVED.

Finally, all roles have access to list_low_stock which lists any items where stock is less than minimum_stock. 

As this is the final version of this project. A more comprehensive program use guide is outlined below.

To start the program, run main.py.
Apon running main,py, the console will display a prompt to enter username. If this is the first time running the program on your device, a default admin account will be created for you. The credentials for this account are as follows:
Username: Admin
Password: Admin123
You can log in with these credentials.

After logging in, You will be greeted with the main menu.
This main menu presents a numbered list of action options.
You may enter the number corresponding to your desired action in order to run that action.

Any further input required will be prompted similiarly.

If you are on an admin account, you will have access to the admin exclusive actions. Here, you can create multiple user accounts with different roles. Apon creation of these user accounts, you can navigate back to the main menu where you have the option to log out. 'Log out' does NOT do the same as 'exit'. 'Exit' will end the entire program, 'log out' will return you back to the log in portion of the program where you are able to log back in with any other user account.
Feel free to experiement with user access levels for different actions using different user accounts.

