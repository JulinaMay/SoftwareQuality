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
from Log_config import logger

from os import system, name
import time

def main():
    Database.create_or_connect_db()
    logger.info("Program started")
    main_menu()
    
def main_menu():
    while True:
        clear()
        # Voor als je nog niet hebt ingelogd?
        print("\n--- Main Menu ---")
        print("1. Create account")
        print("2. Login")
        print("3. Exit")
        
        choice = input("Choose an option (1/2/3): ").strip()
        # choice = "2"

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
    username = input("Enter your username: ")
    password = getpass("Enter your password: ")
    # username = "super_admin"
    # password = "Admin_123?"

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
                logger.warning(f"{first_name} {last_name} tried to login as a user")
                time.sleep(2)
            elif role_level == "member":
                print("Member is not allowed to login")
                logger.warning(f"{first_name} {last_name} tried to login as a member")
                time.sleep(2)
            elif role_level == "consultant":
                logger.info(f"{decrypt_data(private_key(), user_data[3])} {decrypt_data(private_key(), user_data[4])} logged in as a consultant")
                Consultant.menu(username)
            elif role_level == "admin":
                logger.info(f"{decrypt_data(private_key(), user_data[3])} {decrypt_data(private_key(), user_data[4])} logged in as an admin")
                Admin.menu(username)
        else:
            print("Login failed")
            logger.warning("User entered an invalid password")
            time.sleep(2)
    elif username == super_username and password == super_password:
        logger.info("Super admin logged in")
        SuperAdmin.menu()
    else:
        logger.warning("User inputted an invalid username")
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
