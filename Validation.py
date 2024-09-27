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
    integer = False
    inRange = False
    
    try:
        age = int(age)
        integer = True
        if 0 <= age <= 120:
            inRange = True
    except ValueError:
        pass

    if integer and inRange:
        return True
    return False


def validate_gender(gender):
    if gender not in database.Genders:
        return True
    return False


def validate_weight(weight):
    try:
        weight = float(weight)
    except ValueError:
        return True
    if weight < 0 or weight > 300:
        return True
    return False


def validate_street(street):
    pattern = r"^[a-zA-Z]+(?:[ -][a-zA-Z]+)*$" # A-Z, a-z, -, spaties
    if len(street) > 30 or not re.match(pattern, street):
        return True
    return False


def validate_house_number(house_number):
    try:
        house_number = int(house_number)
    except ValueError:
        return True
    if house_number < 0 or house_number > 10000:
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
