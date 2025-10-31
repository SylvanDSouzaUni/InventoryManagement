Version 1.3


This version has introduced a significant amount of functionality. This functionality will be outlined as a list below:

1) Database Functionality:
Add item, remove item, update item, increase stock, decrease stock and  list items have been improved to include database functionality. This means that these functions no longer return strings outlining if the call of the funciton was successful or not, they actually commit changes to a database which stores items. This means, with this version, admins can create items and handle them in a   database which stores them.

2) Item Request Functionality:
Warehouse workers and Engineers can now submit requests for new items. These requests will exist in a requests table which the admin can see. Admin can approve of requests, which will add the requested item and its fields to the items table. Admin can also reject requests which will remove them from the requests table.  When submitting a request, engineers can enter any values for the fields of the item (no validation). Apon aproval, these fields will be validated to ensure they are safe to add to the original items table.

 3) Item Request Approval Functionality (ADMIN):
Admin now has a "manage requests" option in the admin menu. This allows admins to view, approve and reject requests. Apon aproval, admin will be asked if they would like to change any fields of the item (stock, minimum stock, name, sku, etc) before approval. If no, item fields will be validated. If there are any errors, the admin will be prompted to change item field values to adhere to database standards. If admin chooses to change any values before approval, this will be allowed. Items requests which are approved will be added to the items table and removed from the requests table. Items requests which are rejected will be removed from the requests table.

The permissions of each role are outlined below:
ADMIN:
1) list_items
2) add_item
3) update_item
4) remove_item
5) decrease_stock
6) increase_stock
7) manage_users
8) list_user_information
9) admin_actions
10) approve_item_request
11) reject_item_request

WAREHOUSE:
1) list_items
2) update_item
3) increase_stock
4) request_item
5) submit_item_request

ENGINEER:
1) list_items
2) update_item
3) decrease_stock
4) request_item
5) submit_item_request

When running this program, one admin account will be created as the first account.
The credentials are mentioned in the console apon creation. They are as follows:
Username: admin
Password: admin123
After logging in, the main menu will work as earlier. 
GUI is intuiative and user-friendly. You will be prompted for inputs in a clear manner, hence navigation is not neccesary to outline here.
