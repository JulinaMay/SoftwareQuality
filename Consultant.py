import sqlite3

from getpass import getpass
import bcrypt

import member_menu
import time

from validation import *
from super_admin import *

# logging
from log_config import *

# MENU

def menu(username):
    connection = sqlite3.connect("MealManagement.db")
    cursor = connection.cursor()

    cursor.execute("SELECT username, password, role_level FROM Users WHERE username = ?", (username,))
    user_data = cursor.fetchone()

    role_level = user_data[2]

    while True:
        member_menu.clear()
        print(f"Welcome {username} ({role_level})")
        print("\n--- Consultant Menu ---")

        print("1. Update password")
        print("2. Members menu")
        print("3. Logout")
        choice = input("Choose an option (1/2/3): ").strip()

        if choice == "1":
            member_menu.clear()
            update_password(username)
        elif choice == "2":
            member_menu.clear()
            print("\n--- Members Menu ---")

            print("1. Process member request")
            print("2. Modify member")
            print("3. Retrieve member")
            print("4. Go back")
            choice = input("Choose an option (1/2/3/4): ").strip()

            if choice == "1":
                member_menu.clear()
                add_member()
            elif choice == "2":
                member_menu.clear()
                modify_member(username)
            elif choice == "3":
                member_menu.clear()
                search_member()
            elif choice == "4":
                continue
            else:
                member_menu.clear()
                log_activity(f"{username}", "System", "Invalid input in the main menu", "No")
                time.sleep(2)
        elif choice == "3":
            member_menu.clear()
            log_activity(f"{username}", "System", "Program exited", "No")
            time.sleep(2)
            break
        else:
            log_activity(f"{username}", "System", "Invalid input in the main menu", "No")

# ACTIONS

def update_password(username): # TODO: Add validation
    connection = sqlite3.connect("MealManagement.db")
    cursor = connection.cursor()

    member_menu.clear()
    print("\n--- Update Password ---")

    # Login with current password
    cursor.execute("SELECT username, password FROM Users WHERE username =?", (username,))
    user_data = cursor.fetchone()

    # Check if password is correct
    input_password = getpass("Enter your current password: ")
    if not bcrypt.checkpw(input_password.encode('utf-8'), user_data[1]):
        log_activity(username, "Update password" "Incorrect password", "No")
        return False
    else:
        while True:
            member_menu.clear()
            print("\n--- Update Password ---")
            new_password = getpass("Enter your new password: ")
            if (new_password == ""):
                member_menu.clear()
                print("Password can't be empty")
                log_activity(username, "Update password" "Entered nothing", "No")
                time.sleep(2)
                continue
            elif (new_password == input_password):
                member_menu.clear()
                print("New password can't be the same as the old password")
                log_activity(username, "Update password" "Entered same password as the old password", "No")
                time.sleep(2)
                continue
            elif validate_password(new_password):
                member_menu.clear()
                time.sleep(2)
                continue
            else:
                hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                cursor.execute("UPDATE Users SET password = ? WHERE username = ?", (hashed_password, username))
                connection.commit()
                connection.close()
                member_menu.clear()
                print("Password updated successfully")
                log_activity(username, "Update password" f"Password updated successfully for user: '{username}'", "No")
                time.sleep(2)
                break
        return True

def modify_member(username):
    connection = sqlite3.connect("MealManagement.db")
    cursor = connection.cursor()

    while True:
        member_menu.clear()
        print("\n--- Modify Member ---")
        print("1. Add a member")
        print("2. Modify a member")
        print("3. Search for a member")
        print("4. Go back")
        choice = input("Choose an option (1/2/3/4): ").strip()

        # Update member
        if choice == "1":
            member_menu.clear()
            add_member("member")
        # Go back
        elif choice == "2":
            member_menu.clear()
            modify_member("member")
        elif choice == "3":
            member_menu.clear()
            search_member()
        elif choice == "4":
            break
        # Invalid input
        else:
            member_menu.clear()
            log_activity(username, "System", "Invalid input at the modifying menu", "No")
            time.sleep(2)

    connection.close()
