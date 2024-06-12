import sqlite3
from getpass import getpass
import bcrypt
import Main
import time
import random
import Member
from Validation import *
from SuperAdmin import *

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
        print("2. Members menu")
        print("3. Logout")
        choice = input("Choose an option (1/2/3): ").strip()

        if choice == "1":
            Main.clear()
            update_password(username)
        elif choice == "2":
            Main.clear()
            print("\n--- Members Menu ---")

            print("1. Process member request")
            print("2. Modify member")
            print("3. Retrieve member")
            print("4. Go back")
            choice = input("Choose an option (1/2/3/4): ").strip()

            if choice == "1":
                Main.clear()
                add_member()
            elif choice == "2":
                Main.clear()
                modify_member()
            elif choice == "3":
                Main.clear()
                retrieve_member_data()
            elif choice == "4":
                continue
            else:
                Main.clear()
                print("Invalid input")
                time.sleep(2)

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
            elif validate_password(new_password):
                Main.clear()
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


def modify_member():
    connection = sqlite3.connect("MealManagement.db")
    cursor = connection.cursor()

    while True:
        Main.clear()
        print("\n--- Modify Member ---")
        print("1. Add a member")
        print("2. Modify a member")
        print("3. Search for a member")
        print("4. Go back")
        choice = input("Choose an option (1/2/3/4): ").strip()

        # Update member
        if choice == "1":
            Main.clear()
            add_member("member")
        # Go back
        elif choice == "2":
            Main.clear()
            modify_member("member")
        elif choice == "3":
            Main.clear()
            retrieve_member_data()
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
