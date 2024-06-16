# System admin
import sqlite3

from getpass import getpass
import bcrypt

import time

import Main
from SuperAdmin import *

# logging
from Log_config import *

def menu(username):
    
    connection = sqlite3.connect("MealManagement.db")
    cursor = connection.cursor()

    cursor.execute("SELECT username, password, role_level FROM Users WHERE username =?", (username))
    user_data = cursor.fetchone()

    role_level  = user_data[2]

    while True:
        print(f"Welcome {username} ({role_level})")
        print("\n--- System Admin Menu ---")

    #Eigen gegevens
        print("1. Update password")
    #List van users
        print("2. List of users")
    #Add new consultant
    #Modify, update consultant
    #Delete consultant
    #Give consultant temp password
        print("3. Consultant menu")
    #Backup, restore members info, users data
    #See logs
        print("4. System")
    #Add new member
    #Modify or update member
    #Delete member (consultant cant do that)
    # Delete member
    #Search, retriev info of member
        print("5. Member menu")

        choice = input("Choose an option (1/2/3/4/5): ").strip()

        if choice == "1":
            Main.clear()
            update_password(username)
        elif choice == "2":
            Main.clear()
            list_users()
        elif choice == "3":
            Main.clear()
            consultant_menu()
        elif choice == "4":
            system_menu()
        elif choice == "5":
            Main.clear()    
            member_menu()
        else:
            Main.clear()
            log_activity(username, "System", "Invalid input at the modifying menu", "No")
            time.sleep(2)

# Functies
def update_password(username):
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
        log_activity(username, "Update password" "Incorrect password", "No")
        return False
    else:
        while True:
            Main.clear()
            print("\n--- Update Password ---")
            new_password = getpass("Enter your new password: ")
            if (new_password == ""):
                Main.clear()
                print("Password can't be empty")
                log_activity(username, "Update password" "Entered nothing", "No")
                time.sleep(2)
                continue
            elif (new_password == input_password):
                Main.clear()
                print("New password can't be the same as the old password")
                log_activity(username, "Update password" "Entered same password as the old password", "No")
                time.sleep(2)
                continue
            else:
                hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                cursor.execute("UPDATE Users SET password = ? WHERE username = ?", (hashed_password, username))
                connection.commit()
                connection.close()
                Main.clear()
                print("Password updated successfully")
                log_activity(username, "Update password" f"Password updated successfully for user: '{username}'", "No")
                time.sleep(2)
                break
        return True



