import sqlite3
import re

def proces_member_request():
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

    age = int(input("Enter age: "))
    gender = input("Enter Gender: ")
    weight = float(input("Enter weight: "))
    street = input("Enter street: ")
    house_number = int(input("Enter house number: "))
    postal_code = input("Enter postal code: ")
    city = input("Enter city: ")
    country = input("Enter country: ")
    email = input("Enter email: ")
    phone_number = input("Enter phone number: ")

    cursor.execute(f"INSERT INTO Members (user_id, first_name, last_name, age, gender, weight, street, house_number, postal_code, city, country, email, phone_number) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (user_id, first_name, last_name, age, gender, weight, street, house_number, postal_code, city, country, email, phone_number))


    connection.commit()
    connection.close()

def validate_first_name(first_name):
    pattern = r"^[a-zA-Z]+$"
    if len(first_name) > 15 or not re.match(pattern, first_name):
        print("Invalid first name")
        return True
    return False

def validate_last_name(last_name):
    pattern = r"^[a-zA-Z'-](?:[a-zA-Z'-]|\s(?!\s))*[a-zA-Z'-]$"
    if len(last_name) > 20 or not re.match(pattern, last_name):
        print("Invalid last name")
        return True
    return False
