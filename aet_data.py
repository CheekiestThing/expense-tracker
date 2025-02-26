import re
import aet_console as console

def validate_username(_username : str):
    '''Checks if the given username matches the requirements. Otherwise, keep asking for a username.'''
    while (len(_username) < 6):
        console.print_header("Register a new account")
        console.print_message("Error creating user: The username needs to be at least 6 characters long. Please try again.", type="error")
        _username = input_prompt("Enter a username")
    return _username

def validate_password(_password):
    '''Checks if the given password matches the requirements. Otherwise, keep asking for a password.'''
    error_count = 0
    console.display_password_prompt()
    
    #Check if the password contains a number
    if (re.search(r"[0-9]+", _password) == None):
        error_count += 1
        console.print_message("Invalid password: The password must contain at least one number.", type="error")

    #Check if the password contains a lowercase letter
    if (re.search(r"[a-z]+", _password) == None):
        error_count += 1
        console.print_message("Invalid password: The password must contain at least one lowercase letter.", type="error")

    #Check if the password contains an uppercase letter
    if (re.search(r"[A-Z]+", _password) == None):
        error_count += 1
        console.print_message("Invalid password: The password must contain at least one uppercase letter.", type="error")

    #Check if the password contains a special symbol
    if (re.search(r"[^a-zA-Z0-9]+", _password) == None):
        error_count += 1
        console.print_message("Invalid password: The password must contain at least one special symbol.", type="error")

    #Check if the password has less than 6 symbols
    if (len(_password) < 6):
        error_count += 1
        console.print_message("Invalid password: The password needs to be at least 8 characters long.", type="error")

    #Check if the password has more than 20 symbols
    if (len(_password) > 20):
        error_count += 1
        console.print_message("Invalid password: The length of the password cannot exceed 20 characters.", type="error")

    if (error_count > 0):
        _password = input_prompt("Create a new password")
        validate_password(_password)

    return _password

def validate_phone_number(_phone):
    '''Checks if the phone number provided is valid, otherwise keep asking for valid one.'''
    console.display_phone_prompt()
    
    if (re.search(r"(\+49 *|[0]){1}[0-9]{11}", _phone) == None):
        console.print_message("Invalid phone number: Please try again.", type="error")
        _phone = input_prompt("Enter a valid phone number")
        validate_phone_number(_phone)
    return _phone

def input_prompt(text = ""):
    '''Returns a user input. Uses the native input function but features a print reformating for internal consistency.'''
    #if (text != ""):
       # console.print_message(text)
    return input("# " + text + ": ")

def create_user(username : str, password : str, phone : str):
    '''Creates a dictionary representing a user.'''
    new_user = {}
    new_user["username"] = username
    new_user["password"] = password
    new_user["phone"] = phone
    new_user["purchases"] = []
    return new_user

def create_purchase(date_of_purchase : str, item_name : str, weight : float, price : float, quantity : int):
    '''Creates a dictionary representing a purchase.'''
    new_item = {}
    new_item["date_of_purchase"] = date_of_purchase
    new_item["item_name"] = item_name
    new_item["weight"] = weight
    new_item["price"] = price
    new_item["quantity"] = quantity
    return new_item