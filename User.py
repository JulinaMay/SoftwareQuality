import sqlite3
import bcrypt
from getpass import getpass
import bcrypt
import Main

def create_account():
    while True:
        Main.clear()
        print("\n--- Create Account ---")
        userName = input("Enter a username: ")

        connection = sqlite3.connect("MealManagement.db")
        cursor = connection.cursor()
        
        cursor.execute("SELECT username FROM Users Where username =?", (userName,))
        if cursor.fetchone():
            print("Username already exists. Please choose another username.")
            connection.close()
            continue
        
        password = getpass("Enter a password: ")
        firstName = input("Enter your first name: ").strip()
        lastName = input("Enter your last name: ").strip()
        roleLevel = "user"

        # Hash Password
        hashedPassword = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        cursor.execute("""INSERT INTO Users (
                    username, password, first_name, last_name, role_level)
                    VALUES (?, ?, ?, ?, ?)""", (userName, hashedPassword, firstName, lastName, roleLevel)
                    )
        connection.commit()
        connection.close()
        print("Account created successfully!")
        break