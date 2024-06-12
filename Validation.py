import re
import Database

# VALIDATION

def validate_first_name(first_name):
    pattern = r"^[a-zA-Z]+$" # A-Z, a-z
    if len(first_name) > 15 or not re.match(pattern, first_name):
        print("Invalid first name")
        return True
    return False

def validate_last_name(last_name):
    pattern = r"^[a-zA-Z'-](?:[a-zA-Z'-]|\s(?!\s))*[a-zA-Z'-]$" # A-Z, a-z, ', -, spaties
    if len(last_name) > 20 or not re.match(pattern, last_name):
        print("Invalid last name")
        return True
    return False

def validate_age(age):
    try:
        age = int(age)
    except ValueError:
        print("Age must be a number")
        return True
    if age < 0 or age > 120:
        print("Invalid age")
        return True
    return False

def validate_gender(gender):
    if gender not in Database.Genders:
        print("Invalid Gender")
        return True
    return False

def validate_weight(weight):
    try:
        weight = float(weight)
    except ValueError:
        print("Weight must be a number")
        return True
    if weight < 0 or weight > 300:
        print("Invalid weight")
        return True
    return False

def validate_street(street):
    pattern = r"^[a-zA-Z]+(?:[ -][a-zA-Z]+)*$" # A-Z, a-z, -, spaties
    if len(street) > 30 or not re.match(pattern, street):
        print("Invalid street")
        return True
    return False

def validate_house_number(house_number):
    try:
        house_number = int(house_number)
    except ValueError:
        print("House number must be a number")
        return True
    if house_number < 0 or house_number > 10000:
        print("Invalid house number")
        return True
    return False

def validate_postal_code(postal_code):
    pattern = r"^[1-9][0-9]{3} ?[A-Z]{2}$" # 4 cijfers, spatie, 2 hoofdletters
    if not re.match(pattern, postal_code):
        print("Invalid postal code")
        return True
    return False

def validate_city(city):
    if city not in Database.Cities:
        print("Invalid city")
        return True
    return False

def validate_country(country):
    pattern = r"^[A-Z][a-zA-Z]+$" # First letter capital, rest normal
    if len(country) > 30 or not re.match(pattern, country):
        print("Invalid country")
        return True
    return False

def validate_email(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$" # email regex
    if len(email) > 50 or not re.match(pattern, email):
        print("Invalid email")
        return True
    return False

def validate_phone_number(phone_number):
    pattern = r"^\+(?:[0-9] ?){6,14}[0-9]$" # telefoonnummer regex
    if not re.match(pattern, phone_number):
        print("Invalid phone number")
        return True
    return False

def validate_username(username):
    pattern = r"^[a-zA-Z0-9]+$" # A-Z, a-z, 0-9
    if len(username) > 15 or not re.match(pattern, username):
        print("Username must be alphanumeric and at most 15 characters long")
        return True
    return False

def validate_password(password):
    pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).{8,}$" # 1 hoofdletter, 1 kleine letter, 1 cijfer, 8 karakters
    if not re.match(pattern, password):
        print("Password must contain at least 1 uppercase letter, 1 lowercase letter, 1 number and be at least 8 characters long")
        return True
    return False
