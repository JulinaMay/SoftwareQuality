# Accountlevels
import User
import Consultant
import Admin
from SuperAdmin import super_username, super_password
import SuperAdmin

# database
import sqlite3
import Database

# cryptography and hashing
import bcrypt
from getpass import getpass
from Cryptography import *

# logging
from Log_config import logger, log_activity

from os import system, name
import time

def main():
    Database.create_or_connect_db()
    log_activity("System", "Program started", "No", "No") 
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
            logger.info("Program exited")
            log_activity("System", "Program exited", "No", "No")
            break
        else:
            print("Invalid input")
            logger.warning("User entered an invalid input in main menu")
            log_activity("System", "Invalid input in the main menu", "No", "No")

def Login():
    clear()
    print("\n--- Login ---")
    # username = input("Enter your username: ")
    # password = getpass("Enter your password: ")
    username = "super_admin"
    password = "Admin_123?"

    connection = sqlite3.connect("MealManagement.db")
    cursor = connection.cursor()

    cursor.execute("SELECT username, password, first_name, last_name, role_level FROM Users")
    data = cursor.fetchall()
    user_data = []

    for user in data:
        decrypted_username = decrypt_data(private_key(), user[0])
        if decrypted_username == username:
            user_data = user
            break

    # Login validation
    if user_data:
        username   = decrypt_data(private_key(), user_data[0])
        stored_hash = user_data[1]
        first_name  = decrypt_data(private_key(), user_data[2])
        last_name   = decrypt_data(private_key(), user_data[3])
        role_level  = user_data[4]
        if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
            # check wie er is ingelogd en toon verschillende menus
            if role_level == "user":
                print("User is not allowed to login")
                log_activity(username, "Attempted login", f"User {first_name} {last_name} is not allowed to login", "No")
                time.sleep(2)
            elif role_level == "member":
                print("Member is not allowed to login")
                log_activity(username, "Attempted login", f"Member {first_name} {last_name} is not allowed to login", "No")
                time.sleep(2)
            elif role_level == "consultant":
                log_activity(username, "Login successful", f"{first_name} {last_name} (consultant) logged in", "No")
                Consultant.menu(username)
            elif role_level == "admin":
                log_activity(username, "Login successful", f"{first_name} {last_name} (admin) logged in", "No")
                Admin.menu(username)
        else:
            print("Login failed")
            log_activity(username, "Login failed", "Entered invalid password", "No")
            time.sleep(2)
    elif username == super_username and password == super_password:
        log_activity("SuperAdmin", "Login successful", "Super admin logged in", "No")
        SuperAdmin.menu()
    else:
        log_activity(username, "Login failed", "Inputted an invalid username", "No")
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
