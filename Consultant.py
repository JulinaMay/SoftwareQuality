import sqlite3
import re
import Database


# Todo: change role level

def process_member_request():
    connection = sqlite3.connect("MealManagement.db")
    cursor = connection.cursor()

    print(" MEMBER REQUEST\n----------------")

    # Get information from user
    user_found = False
    while user_found == False:
        # Check if first name is valid
        loop = True
        while loop:
            first_name = input("Enter first name: ").strip()
            loop = validate_first_name(first_name)

        # Check if last name is valid
        loop = True
        while loop:
            last_name = input("Enter last name: ").strip()
            loop = validate_last_name(last_name)

        # Check if user exists in Users table
        user_cursor = cursor.execute(f"SELECT * FROM Users WHERE first_name = '{first_name}' AND last_name = '{last_name}'")
        user = user_cursor.fetchone()
        if user is None:
            print("User not found")
        else:
            user_id = user[0]
            user_found = True
    
    # Check if user is already a member
    member = cursor.execute(f"SELECT * FROM Members WHERE user_id = '{user_id}'")
    if member.fetchone() != None:
        print("User is already a member")
        return

    # Check if age is valid
    loop = True
    while loop:
        age = input("Enter age: ").strip()
        loop = validate_age(age)

    # Check if gender is valid
    loop = True
    while loop:
        gender = input("Enter gender (Male, Female, Neither): ").strip().capitalize()
        loop = validate_gender(gender)

    # Check if weight is valid
    loop = True
    while loop:
        weight = input("Enter weight (kg): ").strip()
        loop = validate_weight(weight)

    # Check if street is valid
    loop = True
    while loop:
        street = input("Enter street: ").strip().title()
        loop = validate_street(street)

    # Check if house number is valid
    loop = True
    while loop:
        house_number = input("Enter house number: ").strip()
        loop = validate_house_number(house_number)

    # Check if postal code is valid
    loop = True
    while loop:
        postal_code = input("Enter postal code: ").strip()
        loop = validate_postal_code(postal_code)

    # Check if city is valid
    loop = True
    while loop:
        city = input("Enter city: ").strip().capitalize()
        loop = validate_city(city)

    # Check if country is valid
    loop = True
    while loop:
        country = input("Enter country: ").strip().capitalize()
        loop = validate_country(country)

    # Check if email is valid
    loop = True
    while loop:
        email = input("Enter email: ").strip().lower()
        loop = validate_email(email)

    # Check if phone number is valid
    loop = True
    while loop:
        phone_number = input("Enter phone number: ").strip()
        loop = validate_phone_number(phone_number)

    # Insert member into Members table
    cursor.execute(f"INSERT INTO Members (user_id, first_name, last_name, age, gender, weight, street, house_number, postal_code, city, country, email, phone_number) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (user_id, first_name, last_name, age, gender, weight, street, house_number, postal_code, city, country, email, phone_number))

    # Update role level in Users table
    cursor.execute(f"UPDATE Users SET role_level = 'member' WHERE id = '{user_id}'")

    connection.commit()
    connection.close()

    return (first_name, last_name)

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
