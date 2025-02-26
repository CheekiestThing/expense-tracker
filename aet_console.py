import os
from time import sleep

def clear():
    '''Clears the console.'''
    os.system('cls')

def print_header(text = ""):
    '''Clears the console and prints a line in the header format.'''
    clear()
    print(">>> " + text + " <<<")

def print_message(text : str = "", type : str = "", flush : bool = False, end : str = "\n"):
    '''Prints a line in the message format.'''
    _output = "> " + text

    match type:
        case "error":
            _output = "\033[0;31m" + _output + "\033[1;0m"
        case "confirm":
            _output = "\033[0;32m" + _output + "\033[1;0m"
        case "data":
            _output = "\033[0;34m" + _output + "\033[1;0m"
            
    print(_output, flush = flush, end = end)

def loading_bar():
    '''Creates a loading bar that briefly interupts the program.'''
    sleep(0.5)
    output = "\r█"
    print(output, end="", flush=True)

    sleep(0.5)
    while len(output) < 40:
        output += "█"
        print("\033[1;34m" + output, end="", flush=True)
        sleep(0.00663)

    output += "█"
    print("\033[1;32m" + output + "\033[1;0m", flush=True)
    sleep(1.5)

def display_item(item : dict):
    output = ""
    for key in item:
        match key:
            case "date_of_purchase":
                output += "Date of Purchase: " + item[key]
            case "item_name":
                output += "  Item Name: " + item[key]
            case "price":
                output += "  Price: " + price(item[key])
            case "weight":
                output += "  Weight: " + str(item[key]) + "kg"
            case "quantity":
                output += "  Quantity: " + item[key] + "x"

    if (output != ""):
        print_message(output, type="data")

def price(value : float):
    '''Returns a string representing a price in EUR'''
    return "{:0,.2f}€".format(value)

'''
    Prompts
'''

def display_password_prompt():
    '''Prints the Password prompt.'''
    print_header("Register a new account")
    print_message("Password requirements:")
    print_message("1. Should have at least one number.")
    print_message("2. Should have at least one uppercase and one lowercase character.")
    print_message("3. Should have at least one special symbol.")
    print_message("4. Should be between 6 to 20 characters long.")

def display_phone_prompt():
    '''Prints the Phone number prompt.'''
    print_header("Two-Factor Verification")
    print_message("Lastly, please enter a phone number to verify your identity.")
    print_message("Please note that only German phone numbers can be linked to your account.")
    print_message("Accepted formats: +49XXXXXXXXXXX, 0XXXXXXXXXXX")

def display_login_prompt():
    '''Prints the Log In prompt.'''
    print_header("Log in")

def display_menu():
    '''Prints the first menu prompt.'''
    print_header("Welcome to Amazon!")
    print_message("What would you like to do?")
    print_message("  1. Log in using an existing Account")
    print_message("  2. Create a new Account")
    print_message("  3. Quit")

def display_user_menu():
    '''Prints the User menu prompt.'''
    print_header("User Management")
    print_message("What would you like to do?")
    print_message("  1. Enter a Purchase")
    print_message("  2. Generate a Report")
    print_message("  3. Log off and Quit")

def display_item_prompt(item : dict):
    '''Prints the Item prompt with .'''
    print_header("Enter a Purchase")
    display_item(item)