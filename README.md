Version 1.2

In this version, admin role now has the ability to create and delete users and view all existing users in a tabular format
The menu gui has also changed. All admin exclusive actions are now bundled under an admin menu which you can traverse to in the main menu section. This significantly reduces the number of actions that are shown on the main menu, which is especially beneficial as most roles cannot even complete these actions. Users are now able to log out of the program to log back in with a different account. This means apon first creation, the intial admin account can be used to create multiple different accounts. Then, the admin account can be logged out of, allowing the other users to log in with a different account. Actions can only be completed if the user has the correct permissions. Permissions are outlined below:

Admin: List items, update items, decrease stock, increase stock, add item, remove item, create new user, delete existing user, list all users information.
Engineer: List items, update items, decrease stock.
Warehouse: List items, update items, increase stock.

The code has also been organised and commented clearer to maintain readability. 



When running this program, one admin account will be created as the first account.
The credentials are mentioned in the console apon creation. They are as follows:
Username: admin
Password: admin123
After logging in, the main menu will work as before. 
