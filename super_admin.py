# Database
import sqlite3

# Own modules
import main
import member
import user
# Validation
from validation import *

# Logging
from log_config import logmanager as log_manager
log_instance = log_manager()

# cryptography and hashing
import bcrypt
from safe_data import *

# search
from search import *

import time
from datetime import datetime
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

    #List van users
    while True:
        main.clear()
        log_instance.show_notifications()
        print("\n--- Super Admin Menu ---")
        print(f"--Welcome super admin--\n")
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
        choice = input("Choose an option (1/2/3/4/5/6): ").strip()

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
            member_menu()
        elif choice == "6":
            print("You logged out, Goodbye!")
            log_instance.log_activity(super_username, "System", "Program exited", "No")
            break
        else:
            print("Invalid input")
            log_instance.log_activity(super_username, "System", "Invalid input in the main menu", "No")
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
            log_instance.log_activity(super_username, "List of users", "Invalid input in the list of users", "No")
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

        choice = input("Choose an option (1/2/3/4/5): ")
        
        if choice == "1":
            print("Make a new consultant")
            user.create_account("consultant")
            print("\nAdded a new consultant")
            log_instance.log_activity(super_username, "Add a consultant", "Added a new consultant", "No")
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
        print("2. Modify admin")
        print("3. Delete a admin")
        print("4. Reset password of a admin")
        print("5. Go back")

        choice = input("Choose an option (1/2/3/4/5): ")

        if choice == "1":
            print("Make a new system admin")
            user.create_account("admin")
            print("\nAdded a new admin")
            log_instance.log_activity(super_username, "System admin created", "New system administrator created successfully", "No")
            time.sleep(2)
        elif choice == "2":
            main.clear()
            modify_user("admin")
        elif choice == "3":
            main.clear()
            delete_user("admin")
        elif choice == "4":
            main.clear()
            reset_pw("admin")
        elif choice == "5":
            break
        else:
            print("Invalid input")
            log_instance.log_activity(super_username, "System", "Invalid input in the admin menu", "No")
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
            log_instance.log_activity(super_username, "System", "Backup created", "No")
            time.sleep(2)
        elif choice == "2":
            main.clear()
            print("Are you sure you want to restore the backup? This will delete all current data.")
            choice = input("Choose an option (yes/no): ").strip().lower()
            if choice == "y" or choice == "yes":
                restore_backup(db_path, zip_path)
                log_instance.log_activity(super_username, "System", "Backup restored", "No")
            else:
                print("Action cancelled")
                log_instance.log_activity(super_username, "System", "Backup restore cancelled", "No")
                time.sleep(2)
        elif choice == "3":
            date = input("Keep empty for today's logs or enter the date of the log file you want to see (yyyy-mm-dd): ").strip()
            main.clear()
            log_instance.see_logs(date)
        elif choice == "4":
            break
        else:
            print("Invalid input")
            log_instance.log_activity(super_username, "System", "Invalid input in the system menu", "No")
            time.sleep(2)
        connection.close()

# Member menu
def member_menu():
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
            search_member("member")
        elif choice == "5":
            break
        else:
            print("Invalid input")
            log_instance.log_activity(super_username, "Member menu", "Invalid input in the member menu", "No")
            connection.close()

def modify_data(datatype_to_update, table_to_update, id_to_update, new_data) -> bool:
    connection = sqlite3.connect("mealmanagement.db")
    cursor = connection.cursor()

    new_data = encrypt_data(public_key(), new_data)

    if table_to_update == "Users":
        cursor.execute(f"UPDATE {table_to_update} SET {datatype_to_update} = ? WHERE id = ?", (new_data, id_to_update))
        connection.commit()
    if table_to_update == "Members":
        cursor.execute(f"UPDATE {table_to_update} SET {datatype_to_update} = ? WHERE member_id = ?", (new_data, id_to_update))
        connection.commit()
    
    if cursor.rowcount == 0:
            print(f"No rows found with id {id_to_update}.")
            time.sleep(2)
            return False

    return True

def modify_user(role):
    connection = sqlite3.connect("mealmanagement.db")
    cursor = connection.cursor()
    
    while True:
        main.clear()
        print("\n--- Update user ---")
    
        # Search for user
        if role == "admin" or role == "consultant":
            main.clear()
            search_term = input("Enter search term: ").strip()
            search_results = search(search_term, "Users")
            display_search_results(search_results)
            # menu
            try:
                choice = int(input("\nEnter the number of the result you want to choose (or 0 to cancel): "))
                if choice == 0:
                    print("Operation canceled.")
                    break
                elif 1 <= choice <= len(search_results):
                    selected_result = search_results[choice]
                    main.clear()
                    print(f"Selected user: {selected_result[1]}")
                else:
                    print("Invalid choice. Please select a valid number.")
                    input("Press enter to continue")
                    continue
            except ValueError:
                print("Please enter a number.")
                input("Press enter to continue.")
                continue
            
            while True:
                print("\n 1. Username")
                print(" 2. First name")
                print(" 3. Last name")
                choice = input("\nChoose the datatype you want to change (1/2/3): ")
                if choice == "1":
                    new_data = input("\nEnter new username: ").strip()
                    if modify_data("username", "Users", selected_result[0], new_data):
                        main.clear()
                        print("Username updated successfully")
                        time.sleep(2)
                        break
                    else:
                        print("Username not updated")
                        break
                elif choice == "2":
                    new_data = input("\nEnter new first name: ").strip()
                    if modify_data("first_name", "Users", selected_result[0], new_data):
                        main.clear()
                        print("First name updated successfully")
                        time.sleep(2)
                        break
                    else:
                        print("First name not updated")
                        break 
                elif choice == "3":
                    new_data = input("\nEnter new last name: ").strip()
                    if modify_data("last_name", "Users", selected_result[0], new_data):
                        main.clear()
                        print("Last name updated successfully")
                        time.sleep(2)
                        break
                    else:
                        print("Last name not updated")
                        break
                else:
                    print("Invalid input")
                    time.sleep(2)
                    continue
        
        # Search for member
        elif role == "member":
            search_term = input("Enter search term: ").strip()
            search_results = search(search_term, "Members")
            if (len(search_results) == 0):
                main.clear()
                print("No members found")
                time.sleep(2)
                return
            else:
                member_to_update = show_members(search_results[1:], from_modify=True)
                # choose datatype
                while True:
                    main.clear()
                    print("\n 1. First name")
                    print(" 2. Last name")
                    print(" 3. Age")
                    print(" 4. Gender")
                    print(" 5. Weight")
                    print(" 6. Street")
                    print(" 7. House number")
                    print(" 8. Postal code")
                    print(" 9. City")
                    print("10. Country")
                    print("11. Email")
                    print("12. Phone number")
                    choice = input("Choose the datatype you want to change (1/2/3/4/5/6/7/8/9/10/11/12): ")
                    if choice == "1":
                        new_data = input("Enter new first name: ").strip()
                        if modify_data("first_name", "Members", member_to_update, new_data):
                            main.clear()
                            print("First name updated successfully")
                            time.sleep(2)
                            break
                        else:
                            print("First name not updated")
                            time.sleep(2)
                            break
                    elif choice == "2":
                        new_data = input("Enter new last name: ").strip()
                        if modify_data("last_name", "Members", member_to_update, new_data):
                            main.clear()
                            print("Last name updated successfully")
                            time.sleep(2)
                            break
                        else:
                            print("Last name not updated")
                            time.sleep(2)
                            break
                    elif choice == "3":
                        new_data = input("Enter new age: ").strip()
                        if modify_data("age", "Members", member_to_update, new_data):
                            main.clear()
                            print("Age updated successfully")
                            time.sleep(2)
                            break
                        else:
                            print("Age not updated")
                            time.sleep(2)
                            break
                    elif choice == "4":
                        new_data = input("Enter new gender: ").strip()
                        if modify_data("gender", "Members", member_to_update, new_data):
                            main.clear()
                            print("Gender updated successfully")
                            time.sleep(2)
                            break
                        else:
                            print("Gender not updated")
                            time.sleep(2)
                            break
                    elif choice == "5":
                        new_data = input("Enter new weight: ").strip()
                        if modify_data("weight", "Members", member_to_update, new_data):
                            main.clear()
                            print("Weight updated successfully")
                            time.sleep(2)
                            break
                        else:
                            print("Weight not updated")
                            time.sleep(2)
                            break
                    elif choice == "6":
                        new_data = input("Enter new street: ").strip()
                        if modify_data("street", "Members", member_to_update, new_data):
                            main.clear()
                            print("Street updated successfully")
                            time.sleep(2)
                            break
                        else:
                            print("Street not updated")
                            time.sleep(2)
                            break
                    elif choice == "7":
                        new_data = input("Enter new house number: ").strip()
                        if modify_data("house_number", "Members", member_to_update, new_data):
                            main.clear()
                            print("House number updated successfully")
                            time.sleep(2)
                            break
                        else:
                            print("House number not updated")
                            time.sleep(2)
                            break
                    elif choice == "8":
                        new_data = input("Enter new postal code: ").strip()
                        if modify_data("postal_code", "Members", member_to_update, new_data):
                            main.clear()
                            print("Postal code updated successfully")
                            time.sleep(2)
                            break
                        else:
                            print("Postal code not updated")
                            time.sleep(2)
                            break
                    elif choice == "9":
                        new_data = input("Enter new city: ").strip()
                        if modify_data("city", "Members", member_to_update, new_data):
                            main.clear()
                            print("City updated successfully")
                            time.sleep(2)
                            break
                        else:
                            print("City not updated")
                            time.sleep(2)
                            break
                    elif choice == "10":
                        new_data = input("Enter new country: ").strip()
                        if modify_data("country", "Members", member_to_update, new_data):
                            main.clear()
                            print("Country updated successfully")
                            time.sleep(2)
                            break
                        else:
                            print("Country not updated")
                            time.sleep(2)
                            break
                    elif choice == "11":
                        new_data = input("Enter new email: ").strip()
                        if modify_data("email", "Members", member_to_update, new_data):
                            main.clear()
                            print("Email updated successfully")
                            time.sleep(2)
                            break
                        else:
                            print("Email not updated")
                            time.sleep(2)
                            break
                    elif choice == "12":
                        new_data = input("Enter new phone number: ").strip()
                        if modify_data("phone_number", "Members", member_to_update, new_data):
                            main.clear()
                            print("Phone number updated successfully")
                            time.sleep(2)
                            break
                        else:
                            print("Phone number not updated")
                            time.sleep(2)
                            break
                    else:
                        print("Invalid input")
                        time.sleep(2)
            return
            
        else:
            main.clear()
            print("Invalid input")
            time.sleep(2)
              
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
            log_instance.log_activity(super_username, "Delete user", f"Deleted {role} with name: {decrypted_name}", "No")
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

            log_instance.log_activity(super_username, "Reset password", f"Reset password of {role} with username: {decrypted_name}", "No")
            time.sleep(2)
            break

def add_member():
    connection = sqlite3.connect("mealmanagement.db")
    cursor = connection.cursor()

    main.clear()
    print("\n--- Process member Request ---")

    # Input and validation
    first_name = input_and_validate("Enter first name: ", validate_first_name, "Karlijn")
    last_name = input_and_validate("Enter last name: ", validate_last_name, "hofman")
    age = input_and_validate("Enter age: ", validate_age, "19")
    gender = input_and_validate("Enter gender (Male, Female, Neither): ", validate_gender, "Male")
    weight = input_and_validate("Enter weight (kg): ", validate_weight, "80")
    street = input_and_validate("Enter street: ", validate_street, "abc")
    house_number = input_and_validate("Enter house number: ", validate_house_number, "99")
    postal_code = input_and_validate("Enter postal code: ", validate_postal_code, "1234AB")
    city = input_and_validate("Enter city: ", validate_city, "Rotterdam")
    country = input_and_validate("Enter country: ", validate_country, "Nederland")
    email = input_and_validate("Enter email: ", validate_email, "karlijn@gmail.com")
    phone_number = input_and_validate("Enter phone number: ", validate_phone_number, "+31 6 12345678")
    
    #  Create unique member_id
    current_date = str(datetime.now().year)
    print(type(current_date))
    print(current_date[-2:])
    member_id = current_date[-2:]
    print(member_id)

    checksum = sum(int(digit) for digit in member_id)
    for i in range(7):
        random_number = random.randint(0, 9)
        member_id += str(random_number) 
        checksum += random_number

    checksum %= 10
    member_id += str(checksum)
    print(f"stopt het hier? {member_id}")
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
    print(f"member_id: {member_id}, type: {type(member_id)}")

    # Insert member into Members table
    cursor.execute(
        """
        INSERT INTO Members (
            member_id, first_name, last_name, age, gender, weight, street,
            house_number, postal_code, city, country, email, phone_number
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, 
        (member_id, enc_first_name, enc_last_name, enc_age, enc_gender, enc_weight, enc_street, enc_house_number, enc_postal_code, enc_city, enc_country, enc_email, enc_phone_number)
    )

    connection.commit()
    connection.close()

    main.clear()
    print("Member request processed successfully")
    log_instance.log_activity(super_username, "Add member", f"Added member: '{first_name} {last_name}'", "No")
    time.sleep(2)

    return (first_name, last_name)
    
def input_and_validate(prompt, validate_func, default_value=""):
    data = default_value or input(prompt).strip()
    if validate_func(data):
        return data
    else:
        print("Invalid input provided.")
        log_instance.log_activity("System", "Invalid input", "Validation did not pass", "No")

def search_member(role):
    connection = sqlite3.connect("mealmanagement.db")
    cursor = connection.cursor()
    while True:
        if role == "member":
                search_term = input("Enter search term: ").strip()
                search_results = search(search_term, "Members")
                if (len(search_results) == 0):
                    main.clear()
                    print("No members found")
                    time.sleep(2)
                    return
                else:
                    show_members(search_results[1:], from_modify=False)
        else:
            main.clear()
            print("Invalid input")
            time.sleep(2)

def show_members(members, from_modify=False):
    
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
        print(f"\n--- page {current_member + 1} / {len(members)} ---")
        print("N. Next member")
        print("P. Previous member")
        print("B. Go back")
        if from_modify:
            print("\nEnter the pagenumber of the member you want to update (or N/P for another member): ")
        choice = input("Choose an option: ").strip()
        if choice.lower() == "n" or choice.lower() == "no":
            if current_member == len(members) - 1:
                main.clear()
                print("You have reached the last page")
                time.sleep(2)
            else:
                current_member += 1
        elif choice.lower() == "p":
            if current_member == 0:
                main.clear()
                print("You are already at the first page")
                time.sleep(2)
            else:
                current_member -= 1
        elif choice.lower() == "b":
            member_menu()
        else:
            member_to_update = choice
            try:
                member_to_update = int(choice) - 1
                if member_to_update < 0 or member_to_update >= len(members):
                    main.clear()
                    print("Invalid input")
                    log_instance.log_activity(super_username, "Search member", "Invalid input in the search member menu", "No")
                    time.sleep(2)
                    continue
                return members[int(member_to_update)][0]
            except:
                main.clear()
                print("Invalid input")
                time.sleep(2)
                return


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
