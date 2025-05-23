import sqlite3

import time

import bcrypt
from getpass import getpass
from safe_data import *

from validation import *

import main

# logging.
from log_config import logmanager as log_manager
log_instance = log_manager()

def create_account(role):
    while True:
        main.clear()
        print("\n--- Create Account ---")

        # input username
        while True:
            main.clear()
            userName = input("Enter a username: ")
            if validate_username(userName):
                break
            else:
                print("Invalid username. Please try again.")
                time.sleep(2)
                log_instance.log_activity(f"", "Create account failed", "Invalid username", "No")

        connection = sqlite3.connect("mealmanagement.db")
        cursor = connection.cursor()
        
        cursor.execute("SELECT username FROM Users Where username =?", (userName,))
        if cursor.fetchone():
            print("Username already exists. Please choose another username.")
            log_instance.log_activity("", "Create account failed", "Entered already existing username", "No")
            connection.close()
            continue
        
        # input password
        while True:
            main.clear()
            password = getpass("Enter a password: ")
            if validate_password(password):
                break
            else:
                print("Invalid password. Please try again.")
                time.sleep(2)
                log_instance.log_activity("", "Create account failed", "Invalid password", "No")

        # input first name
        while True:
            main.clear()
            firstName = input("Enter your first name: ").strip()
            if validate_first_name(firstName):
                break
            else:
                print("Invalid first name. Please try again.")
                time.sleep(2)
                log_instance.log_activity("", "Create account failed", "Invalid first name", "No")

        # input last name
        while True:
            main.clear()
            lastName = input("Enter your last name: ").strip()
            if validate_last_name(lastName):
                break
            else:
                print("Invalid last name. Please try again.")
                time.sleep(2)
                log_instance.log_activity("", "Create account failed", "Invalid last name", "No")

        if role == "member":
            roleLevel = "member"
        elif role == "consultant":
            roleLevel = "consultant"
        elif role == "admin":
            roleLevel = "admin"
        else:
            roleLevel = "user"
        # Hash Password
        hashedPassword = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # encrypt data
        enc_username = encrypt_data(public_key(), userName)
        enc_firstName = encrypt_data(public_key(), firstName)
        enc_lastName = encrypt_data(public_key(), lastName)

        cursor.execute("""INSERT INTO Users (
                    username, password, first_name, last_name, role_level)
                    VALUES (?, ?, ?, ?, ?)""", (enc_username, hashedPassword, enc_firstName, enc_lastName, roleLevel)
                    )
        connection.commit()

        connection.close()
        log_instance.log_activity("", "Acount created", f"Account created successfully with the username: '{userName}'", "No")
        break
