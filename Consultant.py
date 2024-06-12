import sqlite3
from getpass import getpass
import bcrypt
import Main
import time
import random
import Member
from Validation import *

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
    Main.clear()
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
        while True:
            Main.clear()
            print("\n--- Update Password ---")
            new_password = getpass("Enter your new password: ")
            if (new_password == ""):
                Main.clear()
                print("Password can't be empty")
                time.sleep(2)
                continue
            elif (new_password == input_password):
                Main.clear()
                print("New password can't be the same as the old password")
                time.sleep(2)
                continue
            else:
                hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                cursor.execute("UPDATE Users SET password = ? WHERE username = ?", (hashed_password, username))
                connection.commit()
                connection.close()
                Main.clear()
                print("Password updated successfully")
                time.sleep(2)
                break
        return True

def process_member_request():
    connection = sqlite3.connect("MealManagement.db")
    cursor = connection.cursor()

    print("\n--- Process Member Request ---")

    # Get information from user
    user_found = False
    while user_found == False:
        id = input("Enter user id: ").strip()

        # Check if user exists in Users table
        user_cursor = cursor.execute(f"SELECT * FROM Users WHERE id = '{id}'")
        user = user_cursor.fetchone()
        if user is None:
            print("User not found")
        else:
            user_found = True
    
    # Check if user is already a member
    cursor.execute(f"SELECT * FROM Members WHERE user_id = '{id}'")
    member = cursor.fetchall()
    if member != []:
        print("User is already a member")
        return
    
    # Get user fullname
    first_name = user[3]
    last_name = user[4]

    Main.clear()
    print("\n--- Process member Request ---")
    print(f"User: {first_name} {last_name}\n")

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
    user_registration_year = user[5].split("-")[0]
    member_id = str(user_registration_year[-2:])
    checksum = 0
    for i in range(7):
        random_number = random.randint(0, 9)
        member_id += str(random_number) 
        checksum += random_number
    checksum %= 10
    member_id += str(checksum)

    # Insert member into Members table
    cursor.execute(f"INSERT INTO Members (member_id, user_id, first_name, last_name, age, gender, weight, street, house_number, postal_code, city, country, email, phone_number) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (member_id, id, first_name, last_name, age, gender, weight, street, house_number, postal_code, city, country, email, phone_number))

    # Update role level in Users table
    cursor.execute(f"UPDATE Users SET role_level = 'member' WHERE id = '{id}'")

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
        # print("3. Delete user")
        print("3. Go back")
        choice = input("Choose an option (1/2/3/4): ").strip()

        # Update member
        if choice == "1":
            Main.clear()
            print("\n--- Update member ---")
            id_to_update = input("Enter user id of the member you want to update: ").strip()
            
            cursor.execute("SELECT * FROM Members WHERE user_id = ?", (id_to_update,))
            user = cursor.fetchall()

            if user == []:
                Main.clear()
                print("User not found")
                time.sleep(2)
                continue
            else:
                datatype_to_update = input("Enter the datatype you want to update: ").strip()
                print("""List of datatypes:
                      first_name
                      last_name
                      age
                      gender
                      weight
                      street
                      house_number
                      postal_code
                      city
                      country
                      email
                      phone_number
                      """)
                if datatype_to_update == "first_name":
                    loop = True
                    while loop:
                        first_name = input("Enter new first name: ").strip()
                        loop = validate_first_name(first_name)
                        # update member
                        if not loop:
                            cursor.execute("UPDATE Members SET first_name = ? WHERE user_id = ?", (first_name, id_to_update))
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
                            cursor.execute("UPDATE Members SET last_name = ? WHERE user_id = ?", (last_name, id_to_update))
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
                            cursor.execute("UPDATE Members SET age = ? WHERE user_id = ?", (age, id_to_update))
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
                            cursor.execute("UPDATE Members SET gender = ? WHERE user_id = ?", (gender, id_to_update))
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
                            cursor.execute("UPDATE Members SET weight = ? WHERE user_id = ?", (weight, id_to_update))
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
                            cursor.execute("UPDATE Members SET street = ? WHERE user_id = ?", (street, id_to_update))
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
                            cursor.execute("UPDATE Members SET house_number = ? WHERE user_id = ?", (house_number, id_to_update))
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
                            cursor.execute("UPDATE Members SET postal_code = ? WHERE user_id = ?", (postal_code, id_to_update))
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
                            cursor.execute("UPDATE Members SET city = ? WHERE user_id = ?", (city, id_to_update))
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
                            cursor.execute("UPDATE Members SET country = ? WHERE user_id = ?", (country, id_to_update))
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
                            cursor.execute("UPDATE Members SET email = ? WHERE user_id = ?", (email, id_to_update))
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
                            cursor.execute("UPDATE Members SET phone_number = ? WHERE user_id = ?", (phone_number, id_to_update))
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
            id_to_delete = input("Enter user id: ").strip()

            cursor.execute("SELECT * FROM Members WHERE user_id = ?", (id_to_delete))
            member = cursor.fetchall()
            member = member[0]

            if member == []:
                Main.clear()
                print("Member not found")
                time.sleep(2)
                continue
            else:
                sure = input(f"Are you sure you want to delete {member[2]} {member[3]} from member list? (y/n): ").strip().lower()
                if sure == "y":
                    Main.clear()
                    cursor.execute("DELETE FROM Members WHERE user_id = ?", (id_to_delete))
                    cursor.execute("UPDATE Users SET role_level = 'user' WHERE user_id = ?", (id_to_delete))
                    connection.commit()
                    print(f"{member[2]} {member[3]} deleted from member list")
                    time.sleep(2)
                elif sure == "n":
                    Main.clear()
                    print("No member deleted")
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
            id_to_delete = input("Enter id: ").strip()

            cursor.execute("SELECT * FROM Users WHERE user_id = ?", (id_to_delete))
            user = cursor.fetchall()
            user = user[0]

            if user == []:
                print("User not found")
                time.sleep(2)
                continue
            else:
                sure = input(f"Are you sure you want to delete {user[2]} {user[4]}? (y/n): ").strip().lower()
                if sure == "y":
                    Main.clear()
                    cursor.execute("DELETE FROM Users WHERE id = ?", (id_to_delete))
                    cursor.execute("DELETE FROM Members WHERE user_id = ?", (id_to_delete))
                    connection.commit()
                    print(f"{user[2]} {user[3]} deleted successfully")
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

    Main.clear()
    print("\n--- Retrieve Member Data ---")
    Main.clear()
    print("\n--- Retrieve member ---")
    search = input("Search: ").strip()
    search = f"%{search}%"

    cursor.execute(f"SELECT * FROM Members WHERE first_name LIKE ?", (search,))
    members = cursor.fetchall()
    
    # Check if any members are found
    if members == []:
        Main.clear()
        print("No members found")
        time.sleep(2)
        return

    current_member = 0
    # Show user data
    while True:
        Main.clear()
        print("\n--- Member Data ---")
        
        # Show member data
        Member.ShowData(members[current_member])
        
        # Show page number and menu
        print("\n--- page", current_member + 1, "/", len(members), "---")
        print("1. Next member")
        print("2. Previous member")
        print("3. Go back")
        choice = input("Choose an option (1/2/3): ").strip()
        if choice == "1":
            if current_member == len(members) - 1:
                Main.clear()
                print("You have reached the last page")
                time.sleep(2)
            else:
                current_member += 1
        elif choice == "2":
            if current_member == 0:
                Main.clear()
                print("You are already at the first page")
                time.sleep(2)
            else:
                current_member -= 1
        elif choice == "3":
            break
        else:
            Main.clear()
            print("Invalid input")
            time.sleep(2)
    connection.close()
