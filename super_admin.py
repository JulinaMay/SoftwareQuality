# Database
import sqlite3

# Own modules
import main
import member
import user
# Validation
from validation import *

# Logging
from log_config import *

# cryptography and hashing
import bcrypt
from safe_data import *

import time
import datetime
import random
import zipfile
import os
import shutil

# Hardcoded gegevens
super_username="super_admin"
super_password="Admin_123?"

def menu():
    main.clear()
    connection = sqlite3.connect("mealmanagement.db")
    cursor = connection.cursor()

    main.clear()
    print(f"Welcome super admin!")
    print("\n--- Super Admin Menu ---")
    #List van users
    while True:
        main.clear()
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
        print("6. Logout")
        choice = input("Choose an option (1/2/3/4/5): ").strip()

        if choice == "1":
            main.clear()
            list_users()
        elif choice == "2":
            main.clear()
            consultant_menu()
        elif choice == "3":
            main.clear()
            systemadmin_menu()
        elif choice == "4":
            main.clear()
            system_menu()
        elif choice == "5":
            main.clear()
            Main()
        elif choice == "6":
            print("You logged out, Goodbye!")
            log_activity(super_username, "System", "Program exited", "No")
            break
        else:
            print("Invalid input")
            log_activity(super_username, "System", "Invalid input in the main menu", "No")
            time.sleep(2)
            connection.close()

# List of users
def list_users():
    connection = sqlite3.connect("mealmanagement.db")
    cursor = connection.cursor()

    # Get user data
    cursor.execute("SELECT id, username, role_level FROM Users")
    user_data = cursor.fetchall()

    # Decrypt data
    decrypted_user_data = []
    for id, username, role in user_data:
        decrypted_username = decrypt_data(private_key(), username)
        decrypted_user_data.append((id, decrypted_username, role))

    page = 0
    rows_per_page = 10
    total_pages = (len(decrypted_user_data) + rows_per_page - 1) // rows_per_page
    while True:
        main.clear()
        print("\n--- List of users ---")

        start_row = page * rows_per_page
        end_row = start_row + rows_per_page
        
        # print(df)
        print(f"{'ID':<5}{'Username':<25}{'Role':<10}")
        print("-" * 40)

        for id, username, role in decrypted_user_data[start_row:end_row]:
            print(f"{id:<5}{username:<25}{role:<10}")

        print(f"\n--- page {page + 1} / {total_pages} ---")
        print("1. Next page")
        print("2. Previous page")
        print("3. Go back")
        choice = input("Choose an option (1/2/3): ").strip()
        if choice == "1":
            if page == total_pages - 1:
                print("You have reached the last page")
                time.sleep(2)
                continue
            else:
                page += 1
        elif choice == "2":
            if page == 0:
                print("You are already at the first page")
                time.sleep(2)
                continue
            else:
                page -= 1
        elif choice == "3":
            main.clear()
            break
        else:
            print("Invalid input")
            log_activity(super_username, "List of users", "Invalid input in the list of users", "No")
            continue
    
    connection.close()

# Consultant menu
def consultant_menu():
    connection = sqlite3.connect("mealmanagement.db")
    cursor = connection.cursor()
    while True:
        main.clear()
        print("\n--- Consultant menu ---")
        print("1. Make a new consultant")
        print("2. Modify consultant")
        print("3. Delete a consultant")
        print("4. Reset password of a consultant")
        print("5. Go back")

        choice = input("Choose an option (1/2/3/4/5/6): ")
        
        if choice == "1":
            print("Make a new consultant")
            user.create_account("consultant")
            print("\nAdded a new consultant")
            log_activity(super_username, "Add a consultant", "Added a new consultant", "No")
            time.sleep(2)
        elif choice == "2":
            main.clear()
            modify_user("consultant")
        elif choice == "3":
            main.clear()
            delete_user("consultant")
        elif choice == "4":
            main.clear()
            reset_pw("consultant")
        elif choice == "5":
            break

# System admin menu
def systemadmin_menu():
    connection = sqlite3.connect("mealmanagement.db")
    cursor = connection.cursor()
    while True:
        main.clear()
        print("\n--- System admin menu ---")
        print("1. Make a new system admin")
        print("2. Make an user an admin")
        print("3. Modify admin")
        print("4. Delete a admin")
        print("5. Reset password of a admin")
        print("6. Go back")

        choice = input("Choose an option (1/2/3/4/5/6): ")

        if choice == "1":
            print("Make a new system admin")
            user.create_account("admin")
            print("\nAdded a new admin")
            log_activity(super_username, "System admin created", "New system administrator created successfully", "No")
            time.sleep(2)
        elif choice == "2":
            main.clear()
            update_role("admin")
        elif choice == "3":
            main.clear()
            modify_user("admin")
        elif choice == "4":
            main.clear()
            delete_user("admin")
        elif choice == "5":
            main.clear()
            reset_pw("admin")
        elif choice == "6":
            break
        else:
            print("Invalid input")
            log_activity(super_username, "System", "Invalid input in the admin menu", "No")
            connection.close()

# System menu
def system_menu():
    connection = sqlite3.connect("mealmanagement.db")
    cursor = connection.cursor()
    while True:
        main.clear()

        # Backup and restore
        if not os.path.exists('backup'):
            os.makedirs('backup')
        db_path = "mealmanagement.db"
        backup_path = "backup/backup.sql"
        zip_path = "backup/backup.zip"
        log_dir = "logs"

        print("\n--- System menu ---")
        print("1. Make a backup")
        print("2. Restore backup")
        print("3. See logs")
        print("4. Go back")

        choice = input("Choose an option (1/2/3/4): ")

        if choice == "1":
            # make_backup(db_path, backup_path)
            # create_zip(backup_path, zip_path)
            create_zip(backup_path, log_dir, zip_path)
            print("Backup created")
            log_activity(super_username, "System", "Backup created", "No")
            time.sleep(2)
        elif choice == "2":
            main.clear()
            print("Are you sure you want to restore the backup? This will delete all current data.")
            choice = input("Choose an option (yes/no): ").strip().lower()
            if choice == "y" or choice == "yes":
                restore_backup(db_path, zip_path)
                log_activity(super_username, "System", "Backup restored", "No")
            else:
                print("Action cancelled")
                log_activity(super_username, "System", "Backup restore cancelled", "No")
                time.sleep(2)
        elif choice == "3":
            date = input("Keep empty for today's logs or enter the date of the log file you want to see (yyyy-mm-dd): ").strip()
            main.clear()
            see_logs(date)
        elif choice == "4":
            break
        else:
            print("Invalid input")
            log_activity(super_username, "System", "Invalid input in the system menu", "No")
            time.sleep(2)
        connection.close()

# Member menu
def Main():
    connection = sqlite3.connect("mealmanagement.db")
    cursor = connection.cursor()
    while True:
        main.clear()
        print("\n--- Member menu ---")
        print("1. Make a member")
        print("2. Modify a member")
        print("3. Delete a member")
        print("4. Search for a member")
        print("5. Go back")

        choice = input("Choose an option (1/2/3/4/5): ")

        if choice == "1":
            main.clear()
            add_member()
        elif choice == "2":
            main.clear()
            modify_user("member")
        elif choice == "3":
            main.clear()
            delete_user("member")
        elif choice == "4":
            main.clear()
            search_member()
        elif choice == "5":
            break
        else:
            print("Invalid input")
            log_activity(super_username, "Member menu", "Invalid input in the member menu", "No")
            connection.close()

def update_role(role):
    connection = sqlite3.connect("mealmanagement.db")
    cursor = connection.cursor()
    # Get information from user
    user_found = False
    while user_found == False:
        id = input("Enter the id of the user to change their role: ").strip()

        # Check if user exists in Users table
        user_cursor = cursor.execute(f"SELECT * FROM Users WHERE id = '{id}'")
        user = user_cursor.fetchone()
        if user is None:
            print("User not found")
        elif role == "member":
            cursor.execute("SELECT * FROM Members WHERE user_id = ?", (id))
            member = cursor.fetchall()
            decrypt_member = decrypt_data(private_key(), member[0][2])
            sure = input(f"Are you sure you want to delete {decrypt_member} from member list? (yes/no): ").strip().lower()
            if sure == "yes" or sure == "y":
                main.clear()
                cursor.execute("DELETE FROM Members WHERE user_id = ?", (id))
                connection.commit()
                print(f"{decrypt_member} deleted from member list")
                log_activity(super_username, "Delete member", f"Deleted member: '{decrypt_member}'", "No")
                time.sleep(2)
            elif sure == "n":
                main.clear()
                print("No member deleted")
                log_activity(super_username, "Delete member", "No member deleted", "No")
                time.sleep(2)
            else:
                main.clear()
                log_activity(super_username, "Update role", "Invalid input in the member menu", "No")
                time.sleep(2)
                continue
        else:
            user_found = True
            cursor.execute(f"UPDATE Users SET role_level = '{role}' WHERE id = '{id}'")
            
            connection.commit()
            connection.close()  
            print("Changed succesfully")
            decrypted_name = decrypt_data(private_key(), user[0][1])
            log_activity(super_username, "Update role", f"Changed user: {decrypted_name} into {role}", "No")
            time.sleep(2)
        break

def modify_user(role):
    connection = sqlite3.connect("mealmanagement.db")
    cursor = connection.cursor()
    
    while True:
        print("\n--- Update user ---")
    
        id_to_update = input("Enter the id of the user you want to update: ").strip()
        
        cursor.execute("SELECT * FROM Users WHERE id = ?", (id_to_update,))
        user = cursor.fetchall()

        if not user:
            main.clear()
            print("User not found")
            time.sleep(2)
            continue

        decrypted_name = decrypt_data(private_key(), user[0][1])
        
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
        else:
            print("""List of fields:
                    username
                    first_name
                    last_name
                """)
        datatype_to_update = input("Enter the field you want to update: ").strip()
        table_to_update = "Members" if role == "member" else "Users"

        if datatype_to_update == "username":
            loop = True
            while loop:
                print(f"Username at the moment: {decrypted_name}")
                username = input("Enter username: ").strip()
                loop = validate_username(username)
                username = encrypt_data(public_key(), username)
                # update member
                if loop:
                    cursor.execute("UPDATE Users SET username = ? WHERE id = ?", (username, id_to_update))
                    connection.commit()
                    print("Username updated successfully")
                    log_activity(super_username, "Update user", f"Updated username of user with username: {decrypted_name}", "No")
                    time.sleep(2)
                    break
        elif datatype_to_update == "first_name":
            loop = True
            while loop:
                first_name = input("Enter new first name: ").strip()
                loop = validate_first_name(first_name)
                # update member
                if not loop:
                    cursor.execute(f"UPDATE Users SET first_name = ? WHERE id = ?", (first_name, id_to_update))
                    connection.commit()

                    if role == "member":
                        cursor.execute("UPDATE Members SET first_name = ? where user_id = ?", (first_name, id_to_update))
                        connection.commit()
                        
                    print("First name updated successfully")
                    log_activity(super_username, "Updated user", f"Updated first name of user with username: {decrypted_name}", "No")
                    time.sleep(2)
                    break
        elif datatype_to_update == "last_name":
            loop = True
            while loop:
                last_name = input("Enter last name: ").strip()
                loop = validate_last_name(last_name)
                # update member
                if not loop:
                    cursor.execute(f"UPDATE {table_to_update} SET last_name = ? WHERE {id_to_update} = ?", (last_name, id_to_update))
                    connection.commit()
                    print("Last name updated successfully")
                    log_activity(super_username, "Update user", f"Updated last name of user with username: {decrypted_name}", "No")
                    time.sleep(2)
                    break
        if role == "member":
            if datatype_to_update == "age":
                    loop = True
                    while loop:
                        age = input("Enter age: ").strip()
                        loop = validate_age(age)
                        # update member
                        if not loop:
                            cursor.execute("UPDATE Members SET age = ? WHERE user_id = ?", (age, id_to_update))
                            connection.commit()
                            print("Age updated successfully")
                            log_activity(super_username, "Update user", f"Updated age of user with username: {decrypted_name}", "No")
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
                        log_activity(super_username, "Update user", f"Updated gender of usre with username: {decrypted_name}", "No")
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
                        log_activity(super_username, "Update user", f"Updated weight of user with username: {decrypted_name}", "No")
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
                        log_activity(super_username, "Update user", f"Updated street of user with username: {decrypted_name}", "No")
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
                        log_activity(super_username, "Update user", f"Updated house number of user with username: {decrypted_name}", "No")
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
                        log_activity(super_username, "Update user", f"Updated postal code of user with username: {decrypted_name}", "No")
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
                        log_activity(super_username, "Update user", f"Updated city of user with username: {decrypted_name}", "No")
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
                        log_activity(super_username, "Update user", f"Updated country of user with username: {decrypted_name}", "No")
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
                        log_activity(super_username, "Update user", f"Updated email of user with username: {decrypted_name}", "No")
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
                        log_activity(super_username, "Update user", f"Updated phone number of user with username: {decrypted_name}", "No")
                        time.sleep(2)
                        break
            else:
                main.clear()
                print("Invalid input")
                log_activity(super_username, "Update user", "Invalid input in modify menu", "No")
                time.sleep(2)
                continue

def delete_user(role):
    connection = sqlite3.connect("mealmanagement.db")
    cursor = connection.cursor()

    while True:
        print(f"\n--- Delete {role} ---")
        id_to_delete = input(f"Enter the id of the {role} you want to delete: ").strip()

        choice = input(f"Are you sure you want to remove {role}? (y/n) ").strip().lower()
        if choice == "n":
            break
        
        cursor.execute("SELECT * FROM Users WHERE id = ?", (id_to_delete,))
        user = cursor.fetchall()
        decrypted_name = decrypt_data(private_key(), user[0][1])

        if user == []:
            main.clear()
            print("User not found")
            time.sleep(2)
            break
        else:
            cursor.execute("DELETE FROM Users WHERE id = ?", (id_to_delete,))
            connection.commit()
            print(f"{role} deleted successfully")
            log_activity(super_username, "Delete user", f"Deleted {role} with name: {decrypted_name}", "No")
            time.sleep(2)
            break

def reset_pw(role):
    main.clear()
    connection = sqlite3.connect("mealmanagement.db")
    cursor = connection.cursor()
    
    while True:
        print(f"\n--- Reset password of {role} ---")
        
        pw_to_delete = input(f"Enter the id of the {role} for the password you want to delete: ").strip()

        cursor.execute("SELECT username, password FROM Users WHERE id = ?", (pw_to_delete,))
        user_to_change = cursor.fetchall()

        if not user_to_change:
            main.clear()
            print("User not found")
            time.sleep(2)
            continue
        else:
            decrypted_name = decrypt_data(private_key(), user_to_change[0][0])
    
            cursor.execute("UPDATE Users SET password = ? WHERE id = ?", (bcrypt.hashpw("Temp_123?".encode('utf-8'), bcrypt.gensalt()), pw_to_delete))
            connection.commit()
            
            print("Password reset successfully")

            log_activity(super_username, "Reset password", f"Reset password of {role} with username: {decrypted_name}", "No")
            time.sleep(2)
            break

def add_member():
    connection = sqlite3.connect("mealmanagement.db")
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
            while True:
                main.clear()
                print("User not found")
                choice = input("Go back? (y/n)").strip().lower()
                if choice == "y":
                    return
                elif choice == "n":
                    break
                else:
                    print("Invalid input")
                    continue
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

    main.clear()
    print("\n--- Process member Request ---")
    print(f"User: {first_name} {last_name}\n")

    # Input and validation
    age = input_and_validate("Enter age: ", validate_age)
    gender = input_and_validate("Enter gender (Male, Female, Neither): ", validate_gender)
    weight = input_and_validate("Enter weight (kg): ", validate_weight)
    street = input_and_validate("Enter street: ", validate_street)
    house_number = input_and_validate("Enter house number: ", validate_house_number)
    postal_code = input_and_validate("Enter postal code: ", validate_postal_code)
    city = input_and_validate("Enter city: ", validate_city)
    country = input_and_validate("Enter country: ", validate_country)
    email = input_and_validate("Enter email: ", validate_email)
    phone_number = input_and_validate("Enter phone number: ", validate_phone_number)
    
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

    main.clear()
    print("Member request processed successfully")
    log_activity(super_username, "Add member", f"Added member: '{first_name} {last_name}'", "No")
    time.sleep(2)

    return (first_name, last_name)

def input_and_validate(prompt, validate_func, default_value=""):
    loop = True
    while loop:
        data = default_value or input(prompt).strip()
        loop = validate_func(data)
    return data

def search_member():
    connection = sqlite3.connect("mealmanagement.db")
    cursor = connection.cursor()

    main.clear()
    print("\n--- Retrieve Member Data ---")
    main.clear()
    print("\n--- Retrieve member ---")
    search = input("Search: ").strip()
    search = f"%{search}%"

    cursor.execute(f"SELECT * FROM Members WHERE user_id LIKE ? OR member_id LIKE ? OR first_name LIKE ? OR last_name LIKE ? OR age LIKE ? OR gender LIKE ? OR weight LIKE ? OR street LIKE ? OR house_number LIKE ? OR postal_code LIKE ? OR city LIKE ? OR country LIKE ? OR email LIKE ? OR phone_number LIKE ?", (search, search, search, search, search, search, search, search, search, search, search, search, search, search))
    members = cursor.fetchall()
    
    # Check if any members are found
    if members == []:
        main.clear()
        print("No members found")
        time.sleep(2)
        return

    current_member = 0
    # Show user data
    while True:
        main.clear()
        print("\n--- Member Data ---")
        
        # Show member data
        member.ShowData(members[current_member])
        
        # Show page number and menu
        print("\n--- page", current_member + 1, "/", len(members), "---")
        print("1. Next member")
        print("2. Previous member")
        print("3. Go back")
        choice = input("Choose an option (1/2/3): ").strip()
        if choice == "1":
            if current_member == len(members) - 1:
                main.clear()
                print("You have reached the last page")
                time.sleep(2)
            else:
                current_member += 1
        elif choice == "2":
            if current_member == 0:
                main.clear()
                print("You are already at the first page")
                time.sleep(2)
            else:
                current_member -= 1
        elif choice == "3":
            break
        else:
            main.clear()
            print("Invalid input")
            log_activity(super_username, "Search member", "Invalid input in the search member menu", "No")
            time.sleep(2)
    connection.close()

def make_backup(backup_path):
    connection = sqlite3.connect("mealmanagement.db")

    with open(backup_path, 'w') as backup_file:
        for line in connection.iterdump():
            backup_file.write('%s\n' % line)

    connection.close()
    
def collect_log_files(log_dir, temp_dir):
    # Create a temporary directory if it doesn't exist
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    
    # Calculate 30 days ago from today
    today = datetime.date.today()
    thirty_days_ago = today - datetime.timedelta(days=30)
    
    # Iterate over log files and copy those modified in the last 30 days
    for filename in os.listdir(log_dir):
        filepath = os.path.join(log_dir, filename)
        if os.path.isfile(filepath):
            modified_time = datetime.date.fromtimestamp(os.path.getmtime(filepath))
            if modified_time >= thirty_days_ago:
                shutil.copy(filepath, temp_dir)

def create_zip(backup_path, log_dir, zip_path):
    temp_dir = 'temp_logs'
    
    # Make a backup of the database
    make_backup(backup_path)
    
    # Collect log files modified in the last 30 days
    collect_log_files(log_dir, temp_dir)
    
    # Create a ZIP file containing both the database backup and log files
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        # Add database backup
        zipf.write(backup_path, os.path.basename(backup_path))
        
        # Add log files
        for log_file in os.listdir(temp_dir):
            log_file_path = os.path.join(temp_dir, log_file)
            zipf.write(log_file_path, os.path.basename(log_file_path))

    # Clean up temporary directory
    shutil.rmtree(temp_dir)

def restore_backup(db_path, zip_path):
    if not os.path.exists(zip_path):
        print("No backup found")
        time.sleep(2)
        return
    else:
        # Connect to the database
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        # Clear the database
        database.clear_database()

        # Extract the backup zip file
        with zipfile.ZipFile(zip_path, 'r') as zipf:
            zipf.extractall('backup')

        # Determine the backup file path
        backup_file_path = os.path.join('backup', 'backup.sql')

        # Read and execute the SQL dump file
        with open(backup_file_path, 'r') as backup_file:
            sql_script = backup_file.read()
            cursor.executescript(sql_script)

        connection.commit()
        connection.close()

        # Cleanup: remove the extracted backup file and directory
        if os.path.exists('backup'):
            for file in os.listdir('backup'):
                os.remove(os.path.join('backup', file))
            os.rmdir('backup')

        print("Backup restored")
        time.sleep(2)

def see_logs(date=None):
    file_path = 'logs/mealmanagement.log'
    if date:
        file_path = f'logs/mealmanagement.log.{date}'

    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            total_lines = len(lines)
            pages = (total_lines + 19) // 20

            page = 0
            while True:
                main.clear()
                start_index = page * 20
                end_index = min((page + 1) * 20, total_lines)
                current_page_lines = lines[start_index:end_index]

                print(f"\n--- Page {page + 1} / {pages} ---\n")
                for line in current_page_lines:
                    print(line.strip())

                print("\n1. Next page")
                print("2. Previous page")
                print("3. Go back")
                choice = input("Choose an option (1/2/3): ").strip()

                if choice == "1":
                    if page < pages - 1:
                        page += 1
                elif choice == "2":
                    if page > 0:
                        page -= 1
                elif choice == "3":
                    break
                else:
                    print("Invalid input")
                    time.sleep(2)
                
    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
        time.sleep(2)
