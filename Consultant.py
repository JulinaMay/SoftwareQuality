import sqlite3
import re
import Database
import getpass
import bcrypt
import Main
import time
import random

# MENU

def menu(username):
    connection = sqlite3.connect("MealManagement.db")
    cursor = connection.cursor()

    cursor.execute("SELECT username, password, role_level FROM Users WHERE username = ?", (username,))
    user_data = cursor.fetchone()

    role_level = user_data[2]

    while True:
        Main.clear()
        print(f"Welcome {username} ({role_level})")
        print("\n--- Consultant Menu ---")

        print("1. Update password")
        print("2. Process member request")
        print("3. Modify member")
        print("4. Retrieve member")
        print("5. Logout")

        choice = input("Choose an option (1/2/3/4/5): ").strip()

        if choice == "1":
            Main.clear()
            update_password(username)
        elif choice == "2":
            Main.clear()
            process_member_request()
        elif choice == "3":
            Main.clear()
            modify_member()
        elif choice == "4":
            Main.clear()
            retrieve_member_data()
        elif choice == "5":
            Main.clear()
            print(f"Logging out. Goodbye {username}!")
            time.sleep(2)
            break
        else:
            print("Invalid input")

# ACTIONS

def update_password(username): # TODO: Add validation
    connection = sqlite3.connect("MealManagement.db")
    cursor = connection.cursor()

    print("\n--- Update Password ---")

    # Login with current password
    cursor.execute("SELECT username, password FROM Users WHERE username =?", (username,))
    user_data = cursor.fetchone()

    # Check if password is correct
    input_password = getpass("Enter your current password: ")
    if not bcrypt.checkpw(input_password.encode('utf-8'), user_data[1]):
        print("Incorrect password")
        return False
    else:
        new_password = getpass("Enter your new password: ")
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        cursor.execute("UPDATE Users SET password = ? WHERE username = ?", (hashed_password, username))
        connection.commit()
        connection.close()
        print("Password updated successfully")
        return True

def process_member_request():
    connection = sqlite3.connect("MealManagement.db")
    cursor = connection.cursor()

    print("\n--- Process Member Request ---")

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

    #  Create unique member_id
    member_id = ""
    checksum = 0
    for i in range(9):
        random_number = random.randint(0, 9)
        member_id += str(random_number) 
        checksum += random_number
    checksum %= 10
    member_id += str(checksum)

    # Insert member into Members table
    cursor.execute(f"INSERT INTO Members (member_id, user_id, first_name, last_name, age, gender, weight, street, house_number, postal_code, city, country, email, phone_number) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (member_id, user_id, first_name, last_name, age, gender, weight, street, house_number, postal_code, city, country, email, phone_number))

    # Update role level in Users table
    cursor.execute(f"UPDATE Users SET role_level = 'member' WHERE id = '{user_id}'")

    connection.commit()
    connection.close()

    Main.clear()
    print("Member request processed successfully")
    time.sleep(2)

    return (first_name, last_name)

def modify_member():
    connection = sqlite3.connect("MealManagement.db")
    cursor = connection.cursor()

    while True:
        Main.clear()
        print("\n--- Modify Member ---")
        print("1. Update member")
        print("2. Delete member")
        print("3. Delete user")
        print("4. Go back")
        choice = input("Choose an option (1/2/3/4): ").strip()

        # Update member
        if choice == "1":
            Main.clear()
            print("\n--- Update member ---")
            first_name_user_to_update = input("Enter the first name of the member you want to update: ").strip()
            last_name_user_to_update = input("Enter the last name of the member you want to update: ").strip()
            user = cursor.execute("SELECT * FROM Members WHERE first_name = ? AND last_name = ?", (first_name_user_to_update, last_name_user_to_update))
            if user.fetchone() == None:
                print("User not found")
                time.sleep(2)
                continue
            else:
                datatype_to_update = input("Enter the datatype you want to update: ").strip()
                if datatype_to_update == "first_name":
                    loop = True
                    while loop:
                        first_name = input("Enter new first name: ").strip()
                        loop = validate_first_name(first_name)
                        # update member
                        if not loop:
                            cursor.execute("UPDATE Members SET first_name = ? WHERE first_name = ? AND last_name = ?", (first_name, first_name_user_to_update, last_name_user_to_update))
                            connection.commit()
                            print("First name updated successfully")
                            time.sleep(2)
                            break
                elif datatype_to_update == "last_name":
                    loop = True
                    while loop:
                        last_name = input("Enter last name: ").strip()
                        loop = validate_last_name(last_name)
                        # update member
                        if not loop:
                            cursor.execute("UPDATE Members SET last_name = ? WHERE first_name = ? AND last_name = ?", (last_name, first_name_user_to_update, last_name_user_to_update))
                            connection.commit()
                            print("Last name updated successfully")
                            time.sleep(2)
                            break
                elif datatype_to_update == "age":
                    loop = True
                    while loop:
                        age = input("Enter age: ").strip()
                        loop = validate_age(age)
                        # update member
                        if not loop:
                            cursor.execute("UPDATE Members SET age = ? WHERE first_name = ? AND last_name = ?", (age, first_name_user_to_update, last_name_user_to_update))
                            connection.commit()
                            print("Age updated successfully")
                            time.sleep(2)
                            break
                elif datatype_to_update == "gender":
                    loop = True
                    while loop:
                        gender = input("Enter gender: ").strip().capitalize()
                        loop = validate_gender(gender)
                        # update member
                        if not loop:
                            cursor.execute("UPDATE Members SET gender = ? WHERE first_name = ? AND last_name =?", (gender, first_name_user_to_update, last_name_user_to_update))
                            connection.commit()
                            print("Gender updated successfully")
                            time.sleep(2)
                            break
                elif datatype_to_update == "weight":
                    loop = True
                    while loop:
                        weight = input("Enter weight: ").strip()
                        loop = validate_weight(weight)
                        # update member
                        if not loop:
                            cursor.execute("UPDATE Members SET weight = ? WHERE first_name = ? AND last_name = ?", (weight, first_name_user_to_update, last_name_user_to_update))
                            connection.commit()
                            print("Weight updated successfully")
                            time.sleep(2)
                            break
                elif datatype_to_update == "street":
                    loop = True
                    while loop:
                        street = input("Enter street: ").strip().title()
                        loop = validate_street(street)
                        # update member
                        if not loop:
                            cursor.execute("UPDATE Members SET street = ? WHERE first_name = ? AND last_name = ?", (street, first_name_user_to_update, last_name_user_to_update))
                            connection.commit()
                            print("Street updated successfully")
                            time.sleep(2)
                            break
                elif datatype_to_update == "house_number":
                    loop = True
                    while loop:
                        house_number = input("Enter house number: ").strip()
                        loop = validate_house_number(house_number)
                        # update member
                        if not loop:
                            cursor.execute("UPDATE Members SET house_number = ? WHERE first_name = ? AND last_name = ?", (house_number, first_name_user_to_update, last_name_user_to_update))
                            connection.commit()
                            print("House number updated successfully")
                            time.sleep(2)
                            break
                elif datatype_to_update == "postal_code":
                    loop = True
                    while loop:
                        postal_code = input("Enter postal code: ").strip()
                        loop = validate_postal_code(postal_code)
                        # update member
                        if not loop:
                            cursor.execute("UPDATE Members SET postal_code = ? WHERE first_name = ? AND last_name = ?", (postal_code, first_name_user_to_update, last_name_user_to_update))
                            connection.commit()
                            print("Postal code updated successfully")
                            time.sleep(2)
                            break
                elif datatype_to_update == "city":
                    loop = True
                    while loop:
                        city = input("Enter city: ").strip().capitalize()
                        loop = validate_city(city)
                        # update member
                        if not loop:
                            cursor.execute("UPDATE Members SET city = ? WHERE first_name = ? AND last_name = ?", (city, first_name_user_to_update, last_name_user_to_update))
                            connection.commit()
                            print("City updated successfully")
                            time.sleep(2)
                            break
                elif datatype_to_update == "country":
                    loop = True
                    while loop:
                        country = input("Enter country: ").strip().capitalize()
                        loop = validate_country(country)
                        # update member
                        if not loop:
                            cursor.execute("UPDATE Members SET country = ? WHERE first_name = ? AND last_name = ?", (country, first_name_user_to_update, last_name_user_to_update))
                            connection.commit()
                            print("Country updated successfully")
                            time.sleep(2)
                            break
                elif datatype_to_update == "email":
                    loop = True
                    while loop:
                        email = input("Enter email: ").strip().lower()
                        loop = validate_email(email)
                        # update member
                        if not loop:
                            cursor.execute("UPDATE Members SET email = ? WHERE first_name = ? AND last_name = ?", (email, first_name_user_to_update, last_name_user_to_update))
                            connection.commit()
                            print("Email updated successfully")
                            time.sleep(2)
                            break
                elif datatype_to_update == "phone_number":
                    loop = True
                    while loop:
                        phone_number = input("Enter phone number: ").strip()
                        loop = validate_phone_number(phone_number)
                        # update member
                        if not loop:
                            cursor.execute("UPDATE Members SET phone_number = ? WHERE first_name = ? AND last_name = ?", (phone_number, first_name_user_to_update, last_name_user_to_update))
                            connection.commit()
                            print("Phone number updated successfully")
                            time.sleep(2)
                            break
                else:
                    Main.clear()
                    print("Invalid input")
                    time.sleep(2)
                    continue
        # Delete member
        elif choice == "2":
            Main.clear()
            print("\n--- Delete member ---")
            first_name_member_to_delete = input("Enter first name: ").strip()
            last_name_member_to_delete = input("Enter last name: ").strip()
            user = cursor.execute("SELECT * FROM Members WHERE first_name = ? AND last_name = ?", (first_name_member_to_delete, last_name_member_to_delete))
            if user.fetchone() == None:
                print("User not found")
                time.sleep(2)
                continue
            else:
                sure = input(f"Are you sure you want to delete {first_name_member_to_delete} {last_name_member_to_delete}? (y/n): ").strip().lower()
                if sure == "y":
                    Main.clear()
                    cursor.execute("DELETE FROM Members WHERE first_name = ? AND last_name = ?", (first_name_member_to_delete, last_name_member_to_delete))
                    cursor.execute("UPDATE Users SET role_level = 'user' WHERE first_name = ? AND last_name = ?", (first_name_member_to_delete, last_name_member_to_delete))
                    connection.commit()
                    print(f"{first_name_member_to_delete} {last_name_member_to_delete} deleted successfully")
                    time.sleep(2)
                elif sure == "n":
                    Main.clear()
                    print("No user deleted")
                    time.sleep(2)
                else:
                    Main.clear()
                    print("Invalid input")
                    time.sleep(2)
                    continue
        # Delete user
        elif choice == "3":
            Main.clear()
            print("\n--- Delete user ---")
            first_name_user_to_delete = input("Enter first name: ").strip()
            last_name_user_to_delete = input("Enter last name: ").strip()
            user = cursor.execute("SELECT * FROM Users WHERE first_name = ? AND last_name = ?", (first_name_user_to_delete, last_name_user_to_delete))
            if user.fetchone() == None:
                print("User not found")
                time.sleep(2)
                continue
            else:
                sure = input(f"Are you sure you want to delete {first_name_user_to_delete} {last_name_user_to_delete}? (y/n): ").strip().lower()
                if sure == "y":
                    Main.clear()
                    cursor.execute("DELETE FROM Users WHERE first_name = ? AND last_name = ?", (first_name_user_to_delete, last_name_user_to_delete))
                    cursor.execute("DELETE FROM Members WHERE first_name = ? AND last_name = ?", (first_name_user_to_delete, last_name_user_to_delete))
                    connection.commit()
                    print(f"{first_name_user_to_delete} {last_name_user_to_delete} deleted successfully")
                    time.sleep(2)
                elif sure == "n":
                    Main.clear()
                    print("No user deleted")
                    time.sleep(2)
                else:
                    Main.clear()
                    print("Invalid input")
                    time.sleep(2)
                    continue
        # Go back
        elif choice == "4":
            break
        # Invalid input
        else:
            Main.clear()
            print("Invalid input")
            time.sleep(2)

    connection.commit()
    connection.close()

def retrieve_member_data():
    connection = sqlite3.connect("MealManagement.db")
    cursor = connection.cursor()

    while True:
        Main.clear()
        print("\n--- Retrieve Member Data ---")
        print("1. Retrieve member by name")
        print("2. Retrieve member by id")
        print("3. Go back")
        choice = input("Choose an option (1/2/3): ").strip()

        if choice == "1":
            Main.clear()
            print("Retrieve member by name")
            time.sleep(2)
        elif choice == "2":
            Main.clear()
            print("Retrieve member by member_id")
            time.sleep(2)
        elif choice == "3":
            break
        else:
            Main.clear()
            print("Invalid input")
            time.sleep(2)
    
    connection.close()

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
