import re
import database

# logging
from log_config import logger

# VALIDATION

def validate_first_name(first_name):
    pattern = r"^[a-zA-Z'-]+$" # A-Z, a-z
    length = False
    syntax = False

    if len(first_name) < 15:
        length = True
    if re.match(pattern, first_name):
        syntax = True

    if length and syntax:
        return True
    return False


def validate_last_name(last_name):
    pattern = r"^[a-zA-Z'-](?:[a-zA-Z'-]|\s(?!\s))*[a-zA-Z'-]$" # A-Z, a-z, ', -, spaties
    length = False
    syntax = False

    if len(last_name) < 20:
        length = True
    if re.match(pattern, last_name):
        syntax = True

    if length and syntax:
        return True
    return False


def validate_age(age):
    isInteger = False
    inRange = False
    
    try:
        age = int(age)
        isInteger = True
        if 0 <= age <= 120:
            inRange = True
    except ValueError:
        pass

    if isInteger and inRange:
        return True
    return False


def validate_gender(gender):
    genderExists = False

    if gender in database.Genders:
        genderExists = True

    if genderExists:
        return True
    return False


def validate_weight(weight):
    isFloat = False
    inRange = False


    try:
        weight = float(weight)
        isFloat = True
        if 0 <= weight <= 300:
            inRange = True
    except ValueError:
        pass
    
    if isFloat and inRange:
        return True
    return False


def validate_street(street):
    pattern = r"^[a-zA-Z]+(?:[ -][a-zA-Z]+)*$" # A-Z, a-z, -, spaties
    length = False
    syntax = False  

    if len(street) < 50:
        length = True
    if re.match(pattern, street):
        syntax = True

    if length and syntax:
        return True
    return False



def validate_house_number(house_number):
    isInteger = False   
    inRange = False

    try:
        house_number = int(house_number)
        isInteger = True
        if 0 <= house_number <= 10000:
            inRange = True
    except ValueError:
        return True
    
    if isInteger and inRange:
        return True
    return False


def validate_postal_code(postal_code):
    pattern = r"^[1-9][0-9]{3}[A-Z]{2}$" # 4 cijfers, 2 hoofdletters
    if not re.match(pattern, postal_code):
        return True
    return False


def validate_city(city):
    if city not in database.Cities:
        return True
    return False


def validate_country(country):
    pattern = r"^[A-Z][a-zA-Z]+$" # First letter capital, rest normal
    if len(country) > 30 or not re.match(pattern, country):
        return True
    return False


def validate_email(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$" # email regex
    if len(email) > 50 or not re.match(pattern, email):
        return True
    return False


def validate_phone_number(phone_number):
    pattern = r"^\+(?:[0-9] ?){6,14}[0-9]$" # telefoonnummer regex
    if not re.match(pattern, phone_number):
        return True
    return False


def validate_username(username):
    pattern = r"^[a-zA-Z0-9]+$" # A-Z, a-z, 0-9
    if len(username) > 15 or not re.match(pattern, username):
        return True
    return False


def validate_password(password):
    pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).{8,}$" # 1 hoofdletter, 1 kleine letter, 1 cijfer, 8 karakters
    if not re.match(pattern, password):
        return True
    return False
