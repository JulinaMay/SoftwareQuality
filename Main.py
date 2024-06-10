import sqlite3
import bcrypt
from getpass import getpass
import User
import Consultant
import Admin
from Database import create_or_connect_db
from os import system, name

def main():
    create_or_connect_db()
    clear()
    Consultant.menu("meep")
    # while True:
    #     # Voor als je nog niet hebt ingelogd?
    #     print("\n--- Main Menu ---")
    #     print("1. Create account")
    #     print("2. Login")
    #     print("3. Exit")
        
    #     choice = input("Choose an option (1/2/3): ").strip()

    #     if choice == "1":
    #         User.create_account()
    #     elif choice == "2":
    #         Login()
    #     elif choice == "3":
    #         print("Exiting the program. Goodbye!")
    #         break
    #     else:
    #         print("Invalid input")
    # # Consultant.process_member_request()

def Login():
    response = input("Do you have an account? (y/n) ").strip().lower()
    if response == "y":
        username = input("Enter your username: ")
        password = getpass("Enter your password: ")

        connection = sqlite3.connect("MealManagement.db")
        cursor = connection.cursor()

        cursor.execute("SELECT username, password, role_level FROM Users WHERE username =?", (username,))
        user_data = cursor.fetchone()
        
        # Login validation
        if user_data:
            stored_hash = user_data[1]
            role_level  = user_data[2]
            if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
                print(f"\nLogin succes!")
                print(f"Logged in as {role_level}")
                # check wie er is ingelogd en toon verschillende menus
                if role_level == "consultant":
                    Consultant.menu()
                elif role_level == "admin":
                    Admin.menu(username)
            else:
                print("Login failed")
        else:
            print("Users not found")
        connection.close()

    # Create account
    elif response == "n":
        User.create_account()
    # Invalid input
    else:
        print("Invalid input. Please try again.")
        Login()

def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux
    else:
        _ = system('clear')
    
if __name__ == "__main__":
    main()
