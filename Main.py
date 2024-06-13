import sqlite3
import bcrypt
from getpass import getpass
import User
import Consultant
import Admin
from SuperAdmin import super_username, super_password
import SuperAdmin
import Database
from os import system, name
import time
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from Cryptography import *

def main():
    Database.create_or_connect_db()
    main_menu()
    
def main_menu():
    while True:
        clear()
        # Voor als je nog niet hebt ingelogd?
        print("\n--- Main Menu ---")
        print("1. Create account")
        print("2. Login")
        print("3. Exit")
        
        # choice = input("Choose an option (1/2/3): ").strip()
        choice = "2"

        if choice == "1":
            User.create_account("user")
        elif choice == "2":
            Login()
        elif choice == "3":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid input")

def Login():
    clear()
    print("\n--- Login ---")
    # username = input("Enter your username: ")
    # password = getpass("Enter your password: ")
    username = "super_admin"
    password = "Admin_123?"

    if username != "super_admin":
        username = encrypt_data(public_key(), username)

    connection = sqlite3.connect("MealManagement.db")
    cursor = connection.cursor()

    cursor.execute("SELECT username, password, role_level FROM Users WHERE username =?", (username,))
    user_data = cursor.fetchone()
    
    # Login validation
    if user_data:
        username   = user_data[0]
        stored_hash = user_data[1]
        role_level  = user_data[2]
        if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
            # check wie er is ingelogd en toon verschillende menus
            if role_level == "user":
                print("User is not allowed to login")
                time.sleep(2)
            elif role_level == "member":
                print("Member is not allowed to login")
                time.sleep(2)
            elif role_level == "consultant":
                Consultant.menu(username)
            elif role_level == "admin":
                Admin.menu(username)
        else:
            print("Login failed")
            time.sleep(2)
    elif username == super_username and password == super_password:
        SuperAdmin.menu()
    else:
        print("User not found")
        time.sleep(2)
    connection.close()

def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux
    else:
        _ = system('clear')

if __name__ == "__main__":
    main()
