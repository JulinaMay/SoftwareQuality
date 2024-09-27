import sqlite3

import bcrypt
from getpass import getpass
from safe_data import *

import main

# logging
from log_config import *

def create_account(role):
    while True:
        main.clear()
        print("\n--- Create Account ---")
        userName = input("Enter a username: ")

        connection = sqlite3.connect("MealManagement.db")
        cursor = connection.cursor()
        
        cursor.execute("SELECT username FROM Users Where username =?", (userName,))
        if cursor.fetchone():
            print("Username already exists. Please choose another username.")
            log_activity("", "Create account failed", "Entered already existing username", "No")
            connection.close()
            continue
        
        password = getpass("Enter a password: ")
        firstName = input("Enter your first name: ").strip()
        lastName = input("Enter your last name: ").strip()
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
        print("Account created successfully!")
        log_activity("", "Acount created", f"Account created successfully with the username: '{userName}'", "No")
        break
