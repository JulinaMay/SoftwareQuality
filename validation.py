import re
import database

# validation

def validate_first_name(first_name):
    pattern = r"^[a-zA-Z'-]+$" # A-Z, a-z
    length = False
    syntax = False

    if len(first_name) <= 15:
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
    except ValueError:
        return False
    else:
        isInteger = True

    if 0 <= age <= 120:
        inRange = True

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
    except ValueError:
        return False
    else:
        isFloat = True

    if 0 <= weight <= 300:
        inRange = True
    
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
    except ValueError:
        return False
    else:
        isInteger = True
        
    if 0 <= house_number <= 10000:
        inRange = True
    
    if isInteger and inRange:
        return True
    return False


def validate_postal_code(postal_code):
    pattern = r"^[1-9][0-9]{3}[A-Z]{2}$" # 4 cijfers, 2 hoofdletters
    syntax = False

    if re.match(pattern, postal_code):
        syntax = True

    if syntax:
        return True
    return False


def validate_city(city):
    cityExists = False

    if city in database.Cities:
        cityExists = True

    if cityExists:
        return True
    return False


def validate_country(country):
    pattern = r"^[A-Z][a-zA-Z]+$" # First letter capital, rest normal
    length = False
    syntax = False

    if len(country) < 30:
        length = True
    if re.match(pattern, country):
        syntax = True

    if length and syntax:
        return True
    return False


def validate_email(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$" # email regex
    length = False
    syntax = False

    if len(email) < 50:
        length = True
    if re.match(pattern, email):
        syntax = True

    if length and syntax:
        return True
    return False


def validate_phone_number(phone_number):
    pattern = r"^\+(?:[0-9] ?){6,14}[0-9]$" # telefoonnummer regex
    syntax = False

    if re.match(pattern, phone_number):
        syntax = True

    if syntax:
        return True
    return False


def validate_username(username):
    pattern = r"^[a-zA-Z0-9]+$" # A-Z, a-z, 0-9
    syntax = False

    if re.match(pattern, username):
        syntax = True

    if syntax:
        return True
    return False


def validate_password(password):
    pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).{8,}$" # 1 hoofdletter, 1 kleine letter, 1 cijfer, 8 karakters
    syntax = False

    if re.match(pattern, password):
        syntax = True

    if syntax:
        return True
    return False
