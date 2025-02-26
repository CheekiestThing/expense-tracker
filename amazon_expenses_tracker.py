import sys
import re
from datetime import datetime
from time import sleep

# AET Modules
import aet_console as console
import aet_data as data

# Globals
users = []
current_user = None

def state_boot():
    '''The state of the program during which a user can choose to log in or first create a new account.'''
    global current_user

    console.display_menu()
    option = data.input_prompt()

    while option not in ["1", "2", "3", "OFFLINE"]:
        option = data.input_prompt("Invalid input, please try again.") 

    match (option):
        case "1":
            state_login()
        case "2":
            state_register()
        case "3":
            close_program()
        case "OFFLINE":
            current_user = users[0]
            debug_purchase = data.create_purchase(date_of_purchase="19/06/2013", item_name="Minecraft (Java/Bedrock), digital copy", weight=0, price=29.99, quantity=1)
            current_user["purchases"].append(debug_purchase)
            debug_purchase = data.create_purchase(date_of_purchase="26/06/2013", item_name="GeForce GTX 780 graphics card", weight=1.77, price=575, quantity=1)
            current_user["purchases"].append(debug_purchase)
            state_menu()

def close_program():
    '''Displays a thank you message before closing the program.'''
    console.clear()
    console.print_message("Thank you for using the Amazon Expense Tracker! The program is closing now.")
    sleep(2)
    exit()

def state_register(_username = "", _password = "", _phone = ""):
    '''The state of the program during which a user creates a new account.'''
    global users
    newuser = {}
    '''
        Username creation/validation
    '''
    if (_username == ""):
        console.print_header("Register a new account")
        _username = data.input_prompt("Enter a username")

    _username = data.validate_username(_username)

    '''
        Password creation/validation
    '''
    if (_password == ""):
        console.display_password_prompt()
        _password = data.input_prompt("Create a new password")

    _password = data.validate_password(_password)

    if (_phone != ""):
        console.clear()
        console.print_message("Registration complete!")
        sleep(1)

    '''
        Two-Factor-Authentication
    '''
    if (_phone == ""):
        console.display_phone_prompt()
        _phone = data.input_prompt("Enter a valid phone number")

    data.validate_phone_number(_phone)

    # Apply credentials and add the user to the list
    users.append(data.create_user(username=_username, password=_password, phone=_phone))

    console.clear()
    sleep(1)

    console.print_message("Your account has been created!", type="confirm")
    sleep(3)
    state_boot()

def state_login():
    '''The state of the program during which a user tries to log in.'''
    global users
    global current_user
    attempts = 0
    console.display_login_prompt()

    print(users)
    _username = data.input_prompt("Username")
    _password = data.input_prompt("Password")

    while current_user == None:
        console.display_login_prompt()

        for user in users:
            if _username == user["username"]:
                if _password == user["password"]:
                    current_user = user
                    break
        else:
            if current_user == None:
                attempts += 1

                if attempts < 3:
                    console.display_login_prompt()
                    console.print_message("Username and password do not match.", type="error")
                elif attempts == 3:
                    countdown = 5
                    console.display_login_prompt()
                    while countdown > 0:
                        if countdown > 1:
                            console.print_message(f"\rToo many attempts were made at once. Please wait {countdown} seconds and then try again.", type="error", flush=True, end="")
                        else:
                            console.print_message(f"\rToo many attempts were made at once. Please wait {countdown} second and then try again.  ", type="error", flush=True, end="")
                        sleep(1)
                        countdown -= 1
                    console.display_login_prompt()
                elif attempts > 3:
                    console.display_login_prompt()
                    console.print_message("There were too many log in attempts. Please register again. The program is closing now.", type="error")
                    sleep(2)
                    exit()

        if current_user == None:
            _username = data.input_prompt("Username")
            _password = data.input_prompt("Password")

    console.print_header("Log in successful!")
    console.print_message(f"Welcome to the Amazon Expense Tracker, {current_user["username"]}!")
    console.loading_bar()
    state_menu()

def state_menu():
    '''The state of the program during which a logged-in user can choose to add a purchase or get a report.'''
    '''
        state_menu()
    '''
    console.display_user_menu()
    option = data.input_prompt()

    while option not in ["1", "2", "3"]:
        option = data.input_prompt("Invalid input, please try again.") 

    match (option):
        case "1":
            state_enter_purchase()
        case "2":
            state_report()
        case "3":
            close_program()

def state_enter_purchase():
    '''The state of the program during which a user enters a purchase to their system.'''
    new_purchase = {}

    # Date of Purchase
    console.display_item_prompt(new_purchase)
    console.print_message("Accepted formats: MM/DD/YYYY, MM-DD-YYYY")
    console.print_message("Enter the date of purchase")
    date_of_purchase = data.input_prompt().replace("-", "/")

    while True:
        if re.search(r"^[0-9]{2}\/[0-9]{2}\/[0-9]{4}$", date_of_purchase) == None:
            console.display_item_prompt(new_purchase)
            console.print_message("Invalid format. Make sure to enter a valid date", type="error")
            console.print_message("Accepted formats: MM/DD/YYYY, MM-DD-YYYY")
            console.print_message("Enter the date of purchase")
            date_of_purchase = data.input_prompt().replace("-", "/")
        else:
            break
    new_purchase["date_of_purchase"] = date_of_purchase

    # Item Name
    console.display_item_prompt(new_purchase)
    console.print_message("Enter the name of the item:")
    item_name = data.input_prompt()

    while (len(item_name) < 3):
        console.display_item_prompt(new_purchase)
        data.display_item(new_purchase)
        console.print_message("Item names must be at least 3 symbols long.", type="error")
        console.print_message("Enter the name of the item")
        item_name = data.input_prompt()
    new_purchase["item_name"] = item_name

    # Price
    console.display_item_prompt(new_purchase)
    console.print_message("Enter the price of the item")
    price = data.input_prompt()

    while True:
        try:
            float(price)
            break
        except:
            console.display_item_prompt(new_purchase)
            console.print_message("Invalid format. Make sure to enter a valid amount", type="error")
            console.print_message("Enter the price of the item (in EUR)")
            price = data.input_prompt()
    new_purchase["price"] = float(price)

    # Weight
    console.display_item_prompt(new_purchase)
    console.print_message("Enter the weight of the item (in kg)")
    weight = data.input_prompt()

    while True:
        try:
            float(weight)
            break
        except:
            console.display_item_prompt(new_purchase)
            console.print_message("Invalid format. Make sure to enter a valid amount", type="error")
            console.print_message("Enter the weight of the item (in kg)")
            weight = data.input_prompt()
    new_purchase["weight"] = float(weight) 

    #Quantity
    console.display_item_prompt(new_purchase)
    console.print_message("Enter the quantity purchased")
    quantity = data.input_prompt()

    while True:
        try:
            int(quantity)
            break
        except:
            console.display_item_prompt(new_purchase)
            console.print_message("Invalid format. Make sure to enter a valid amount", type="error")
            console.print_message("Enter the quantity purchased")
            quantity = data.input_prompt(
            )
    new_purchase["quantity"] = quantity

    # Save the purchase data to the list
    current_user["purchases"].append(new_purchase)

    # Confirmation message
    console.display_item_prompt(new_purchase)
    console.print_message("Your purchase has been saved!", type="confirm")
    sleep(3)

    state_menu()

def state_report():
    '''The state of the program during which a user receives a report on their purchases.'''
    global current_user

    console.clear()
    console.loading_bar()

    #First, grab the purchases for the current user
    purchases = current_user["purchases"]

    total_item_costs = 0
    total_shipping_costs = 0

    cheapest_order = (99999999999, "N/A", 0, "01/01/1970")
    most_expensive_order = (0, "N/A", 0, "01/01/1970")

    spending_limit = 500
    spending_limit_exceeded = False

    for item in purchases:
        # Calulate the prices for each order
        item_name = item["item_name"]
        quantity = item["quantity"]
        date_of_purchase = item["date_of_purchase"]
        order_cost = float(item["price"])
        shipping_cost = int(float(item["weight"]) * float(item["quantity"]))
        item_cost = max(order_cost - shipping_cost, 0)

        # Add the prices the totals
        total_item_costs += item_cost
        total_shipping_costs += shipping_cost

        # Check if each order is either the cheapest or most expensive order
        if (order_cost > most_expensive_order[0]):
            most_expensive_order = (order_cost, item_name, quantity, date_of_purchase)

        if (order_cost < cheapest_order[0]):
            cheapest_order = (order_cost, item_name, quantity, date_of_purchase)

    # Check if the user has exceeded their spending limit of 500 Euro
    total_costs = total_item_costs + total_shipping_costs
    spending_limit_exceeded = total_costs > spending_limit

    # Get the time of creation for the report and print it out
    creation_date = datetime.now()

    console.print_header("Your Report")
    console.print_message(f"Report created: {creation_date.strftime(f'%Y-%m-%d at %H:%M:%S')}", type="data")
    console.print_message(f"Total costs (without shipping): {console.price(total_item_costs)}", type="data")
    console.print_message(f"Total shipping costs: {console.price(total_shipping_costs)}", type="data")
    if most_expensive_order[1] == "N/A":
        console.print_message(f"Most expensive order: N/A", type="data")
    else:
        console.print_message(f"Most expensive order: {most_expensive_order[2]}x \"{most_expensive_order[1]}\" for {console.price(most_expensive_order[0]) } (ordered on {most_expensive_order[3]})", type="data")
    if cheapest_order[1] == "N/A":
        console.print_message(f"Least expensive order: N/A", type="data")
    else:
        console.print_message(f"Least expensive order: {cheapest_order[2]}x \"{cheapest_order[1]}\" for {console.price(cheapest_order[0])} (ordered on {cheapest_order[3]})", type="data")
    if (spending_limit_exceeded):
        console.print_message(f"You have exceeded your set spending limit of {spending_limit}€ by {console.price(total_costs-spending_limit)}!", type="error")
    else:
        console.print_message(f"You have not exceeded your set spending limit of {spending_limit}€ ({spending_limit-total_costs}€ remaining)", type="confirm")
    data.input_prompt("Enter anything to return to the menu")
    state_menu()

'''
    Main Code starts here
'''

# Additional fake acc for debug
users.append(data.create_user(username="MaxMustermann", password="Müller*Marie64", phone="01783640921"))

# Add an account if enough additional arguments were given on boot
if len(sys.argv) > 3:
    users.append(data.create_user(username=sys.argv[1], password=sys.argv[2], phone=sys.argv[3]))

# Boot up message
console.print_header("Welcome to Amazon!")

console.loading_bar()
state_boot()