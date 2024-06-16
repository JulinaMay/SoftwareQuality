# Database
import sqlite3
import pandas as pd

# Own modules
import Main
import User
import Member

# Validation
from Validation import *

# Logging
from Log_config import logger

# cryptography and hashing
import bcrypt
from Cryptography import *

import time
import random
import zipfile
import os

# Hardcoded gegevens
super_username="super_admin"
super_password="Admin_123?"

def menu():
    
    connection = sqlite3.connect("MealManagement.db")
    cursor = connection.cursor()

    Main.clear()
    print(f"Welcome super admin!")
    print("\n--- Super Admin Menu ---")
    #List van users
    while True:
        Main.clear()
    #List van users
        print("1. List of users")

    #Add new consultant
    #Modify, update consultant
    #Delete consultant
    #Give consultant temp password
        print("2. Consultant menu")

    #Define/Add new system admin
    #Modify, update admin
    #Delete admin
    #Give admin temp password
        print("3. System admin menu")

    #Backup, restore members info, users data
    #See logs
        print("4. System")

    #Add new member
    #Modify or update member
    #Delete member (consultant cant do that)
    # Delete member
    #Search, retriev info of member
        print("5. Member menu")
        print("6. Exit")
        choice = input("Choose an option (1/2/3/4/5): ").strip()

        if choice == "1":
            Main.clear()
            list_users()
        elif choice == "2":
            Main.clear()
            consultant_menu()
        elif choice == "3":
            Main.clear()
            systemadmin_menu()
        elif choice == "4":
            Main.clear()
            system_menu()
        elif choice == "5":
            Main.clear()
            member_menu()
        elif choice == "6":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid input")
            logger.warning("User entered invalid input in super admin menu.")
            time.sleep(2)
            connection.close()

# List of users
def list_users():
    connection = sqlite3.connect("MealManagement.db")
    cursor = connection.cursor()
    while True:
        Main.clear()
        print("\n--- List of users ---")
        # Login with current password
        cursor.execute("SELECT username, role_level FROM Users")
        user_data = cursor.fetchall()

        # TODO: Decrypt data

        df = pd.DataFrame(user_data, columns=["Username", "Role"])
        df.index += 1
        df = df.rename_axis("ID")
        print(df)

        choice = input("\nGo back? (yes/no) ").strip().lower()
        if choice == "yes" or choice == "y":
            Main.clear()
            break
        else:
            print("Try again")
            continue
    connection.close()

# Consultant menu
def consultant_menu():
    connection = sqlite3.connect("MealManagement.db")
    cursor = connection.cursor()
    while True:
        Main.clear()
        print("\n--- Consultant menu ---")
        print("1. Make a new consultant")
        print("2. Make an user a consultant")
        print("3. Modify consultant")
        print("4. Delete a consultant")
        print("5. Reset password of a consultant")
        print("6. Go back")

        choice = input("Choose an option (1/2/3/4/5/6): ")
        
        if choice == "1":
            print("Make a new consultant")
            User.create_account("consultant")
            print("\nAdded a new consultant")
            time.sleep(2)
        elif choice == "2":
            Main.clear()
            update_role("consultant")
        elif choice == "3":
            Main.clear()
            modify_user("consultant")
        elif choice == "4":
            delete_user("consultant")
        elif choice == "5":
            Main.clear()
            reset_pw("consultant")
        elif choice == "6":
            break

# System admin menu
def systemadmin_menu():
    connection = sqlite3.connect("MealManagement.db")
    cursor = connection.cursor()
    while True:
        Main.clear()
        print("\n--- System admin menu ---")
        print("1. Make a new system admin")
        print("2. Make an user an admin")
        print("3. Modify admin")
        print("4. Delete a consultant")
        print("5. Reset password of a consultant")
        print("6. Go back")

        choice = input("Choose an option (1/2/3/4/5/6): ")

        if choice == "1":
            print("Make a new system admin")
            User.create_account("admin")
            print("\nAdded a new admin")
            time.sleep(2)
        elif choice == "2":
            Main.clear()
            update_role("admin")
        elif choice == "3":
            Main.clear()
            modify_user("admin")
        elif choice == "4":
            Main.clear()
            delete_user("admin")
        elif choice == "5":
            Main.clear()
            reset_pw("admin")
        elif choice == "6":
            break
        else:
            print("Invalid input")
            connection.close()

# System menu
def system_menu():
    connection = sqlite3.connect("MealManagement.db")
    cursor = connection.cursor()
    while True:
        Main.clear()
        if not os.path.exists('backup'):
            os.makedirs('backup')
        db_path = "MealManagement.db"
        backup_path = "backup/backup.sql"
        zip_path = "backup/backup.zip"
        print("\n--- System menu ---")
        print("1. Make a backup")
        print("2. Restore backup")
        print("3. See logs")
        print("4. Go back")

        choice = input("Choose an option (1/2/3/4): ")

        if choice == "1":
            make_backup(db_path, backup_path)
            create_zip(backup_path, zip_path)
            print("Backup created")
            time.sleep(2)
        if choice == "2":
            restore_backup(db_path, zip_path)
# Member menu
def member_menu():
    connection = sqlite3.connect("MealManagement.db")
    cursor = connection.cursor()
    while True:
        Main.clear()
        print("\n--- System admin menu ---")
        print("1. Make a member")
        print("2. Modify a member")
        print("3. Delete a member")
        print("4. Search for a member")
        print("5. Go back")

        choice = input("Choose an option (1/2/3/4/5): ")

        if choice == "1":
            Main.clear()
            add_member()
        elif choice == "2":
            Main.clear()
            modify_user("member")
        elif choice == "3":
            Main.clear()
            delete_user("member")
        elif choice == "4":
            Main.clear()
            search_member()
        elif choice == "5":
            break
        else:
            print("Invalid input")
            connection.close()

def update_role(role):
    connection = sqlite3.connect("MealManagement.db")
    cursor = connection.cursor()
    # Get information from user
    user_found = False
    while user_found == False:
        id = input("Enter the id of the user to change their role: ").strip()

        choice = input("Go back? (yes/no)").strip().lower()
        if choice == "y":
            break
        # Check if user exists in Users table
        user_cursor = cursor.execute(f"SELECT * FROM Users WHERE id = '{id}'")
        user = user_cursor.fetchone()
        if user is None:
            print("User not found")
        elif role == "member":
            cursor.execute("SELECT * FROM Members WHERE user_id = ?", (id))
            member = cursor.fetchall()
            member = member[0]
            sure = input(f"Are you sure you want to delete {member[2]} {member[3]} from member list? (y/n): ").strip().lower()
            if sure == "yes" or sure == "y":
                Main.clear()
                cursor.execute("DELETE FROM Members WHERE user_id = ?", (id))
                cursor.execute("UPDATE Users SET role_level = 'user' WHERE user_id = ?", (id))
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
        else:
            user_found = True
            cursor.execute(f"UPDATE Users SET role_level = '{role}' WHERE id = '{id}'")
            
            connection.commit()
            connection.close()  
            print("Changed succesfully")
            time.sleep(2)
        break

def modify_user(role):
    connection = sqlite3.connect("MealManagement.db")
    cursor = connection.cursor()
    
    while True:
        print("\n--- Update user ---")
        id_to_update = input("Enter the id of the user you want to update: ").strip()
        
        cursor.execute("SELECT * FROM Users WHERE id = ?", (id_to_update,))
        user = cursor.fetchall()

        choice = input("Go back? (yes/no) ").strip().lower()
        if choice == "yes" or choice == "y":
            break

        if user == []:
            Main.clear()
            print("User not found")
            time.sleep(2)
            continue
        else:
            print("""List of fields:
                     username
                     first_name
                     last_name
                    """)
            if role == "member":
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
            datatype_to_update = input("Enter the field you want to update: ").strip()

            if datatype_to_update == "username":
                loop = True
                while loop:
                    print(f"Username at the moment: {user[0][1]}")
                    username = input("Enter username: ").strip()
                    loop = validate_username(username)
                    # update member
                    if not loop:
                        cursor.execute("UPDATE users SET username = ? WHERE id = ?", (username, id_to_update))
                        connection.commit()
                        print("Username updated successfully")
                        time.sleep(2)
                        break
            elif datatype_to_update == "first_name":
                loop = True
                while loop:
                    first_name = input("Enter new first name: ").strip()
                    loop = validate_first_name(first_name)
                    # update member
                    if not loop:
                        cursor.execute("UPDATE Members SET first_name = ? WHERE id = ?", (first_name, id_to_update))
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
                        cursor.execute("UPDATE Members SET last_name = ? WHERE id = ?", (last_name, id_to_update))
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
            elif role == "member" and datatype_to_update == "gender":
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
            elif role == "member" and datatype_to_update == "weight":
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
            elif role == "member" and datatype_to_update == "street":
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
            elif role == "member" and datatype_to_update == "house_number":
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
            elif role == "member" and datatype_to_update == "postal_code":
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
            elif role == "member" and datatype_to_update == "city":
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
            elif role == "member" and datatype_to_update == "country":
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
            elif role == "member" and datatype_to_update == "email":
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
            elif role == "member" and datatype_to_update == "phone_number":
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

def delete_user(role):
    connection = sqlite3.connect("MealManagement.db")
    cursor = connection.cursor()

    while True:
        print("\n--- Delete {role} ---")
        id_to_delete = input("Enter the id of the {role} you want to delete: ").strip()
        
        cursor.execute("SELECT * FROM Users WHERE id = ?", (id_to_delete,))
        user = cursor.fetchall()

        choice = input("Go back? (yes/no) ").strip().lower()
        if choice == "yes" or choice == "y":
            break

        if user == []:
            Main.clear()
            print("User not found")
            time.sleep(2)
            continue
        else:
            cursor.execute("DELETE FROM Users WHERE id = ?", (id_to_delete,))
            connection.commit()
            print("Consultant deleted successfully")
            time.sleep(2)

def reset_pw(role):
    Main.clear()
    connection = sqlite3.connect("MealManagement.db")
    cursor = connection.cursor()
    while True:
        print("\n--- Reset password of {role} ---")
        pw_to_delete = input("Enter the id of the {role} for the password you want to delete: ").strip()

        cursor.execute("SELECT password FROM Users WHERE id = ?", (pw_to_delete,))
        user = cursor.fetchall()

        choice = input("Go back? (yes/no) ").strip().lower()
        if choice == "yes" or choice == "y":
            break

        if user == []:
            Main.clear()
            print("User not found")
            time.sleep(2)
            continue
        else:
            cursor.execute("UPDATE Users SET password = ? WHERE id = ?", (bcrypt.hashpw("Temp_123?".encode('utf-8'), bcrypt.gensalt()), pw_to_delete))
            connection.commit()
            print("Password reset successfully")
            time.sleep(2)

def add_member():
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
    
    # decrypt user data
    first_name = decrypt_data(private_key(), user[3])
    last_name = decrypt_data(private_key(), user[4])

    Main.clear()
    print("\n--- Process member Request ---")
    print(f"User: {first_name} {last_name}\n")

    # Input and validation
    age = input_and_validate("Enter age: ", validate_age, "18")
    gender = input_and_validate("Enter gender (Male, Female, Neither): ", validate_gender, "Neither")
    weight = input_and_validate("Enter weight (kg): ", validate_weight, "0")
    street = input_and_validate("Enter street: ", validate_street, "Unknown")
    house_number = input_and_validate("Enter house number: ", validate_house_number, "0")
    postal_code = input_and_validate("Enter postal code: ", validate_postal_code, "1111AA")
    city = input_and_validate("Enter city: ", validate_city, "Groningen")
    country = input_and_validate("Enter country: ", validate_country, "Netherlands")
    email = input_and_validate("Enter email: ", validate_email, "test@test.com")
    phone_number = input_and_validate("Enter phone number: ", validate_phone_number, "+612345678")
    
    #  Create unique member_id
    user_registration_year = user[5].split("-")[0]
    member_id = str(user_registration_year[-2:])
    checksum = sum(int(digit) for digit in member_id)
    for i in range(7):
        random_number = random.randint(0, 9)
        member_id += str(random_number) 
        checksum += random_number
    checksum %= 10
    member_id += str(checksum)

    # encryption
    enc_first_name = encrypt_data(public_key(), first_name)
    enc_last_name = encrypt_data(public_key(), last_name)
    enc_age = encrypt_data(public_key(), age)
    enc_gender = encrypt_data(public_key(), gender)
    enc_weight = encrypt_data(public_key(), weight)
    enc_street = encrypt_data(public_key(), street)
    enc_house_number = encrypt_data(public_key(), house_number)
    enc_postal_code = encrypt_data(public_key(), postal_code)
    enc_city = encrypt_data(public_key(), city)
    enc_country = encrypt_data(public_key(), country)
    enc_email = encrypt_data(public_key(), email)
    enc_phone_number = encrypt_data(public_key(), phone_number)

    # Insert member into Members table
    cursor.execute(
        """
        INSERT INTO Members (
            member_id, user_id, first_name, last_name, age, gender, weight, street,
            house_number, postal_code, city, country, email, phone_number
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, 
        (member_id, id, enc_first_name, enc_last_name, enc_age, enc_gender, enc_weight, enc_street, enc_house_number, enc_postal_code, enc_city, enc_country, enc_email, enc_phone_number)
    )

    # Update role level in Users table
    cursor.execute(f"UPDATE Users SET role_level = 'member' WHERE id = '{id}'")

    connection.commit()
    connection.close()

    Main.clear()
    print("Member request processed successfully")
    time.sleep(2)

    return (first_name, last_name)

def input_and_validate(prompt, validate_func, default_value=""):
    loop = True
    while loop:
        data = default_value or input(prompt).strip()
        loop = validate_func(data)
    return data

def search_member():
    connection = sqlite3.connect("MealManagement.db")
    cursor = connection.cursor()

    Main.clear()
    print("\n--- Retrieve Member Data ---")
    Main.clear()
    print("\n--- Retrieve member ---")
    search = input("Search: ").strip()
    search = f"%{search}%"

    cursor.execute(f"SELECT * FROM Members WHERE user_id LIKE ? OR member_id LIKE ? OR first_name LIKE ? OR last_name LIKE ? OR age LIKE ? OR gender LIKE ? OR weight LIKE ? OR street LIKE ? OR house_number LIKE ? OR postal_code LIKE ? OR city LIKE ? OR country LIKE ? OR email LIKE ? OR phone_number LIKE ?", (search, search, search, search, search, search, search, search, search, search, search, search, search, search))
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

def make_backup(db_path, backup_path):
    connection = sqlite3.connect("MealManagement.db")

    with open(backup_path, 'w') as backup_file:
        for line in connection.iterdump():
            backup_file.write('%s\n' % line)

    connection.close()

def create_zip(backup_path, zip_path):
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        zipf.write(backup_path), os.path.basename(backup_path)

def restore_backup(db_path, zip_path):
    return
