import sqlite3
import bcrypt
from getpass import getpass
# import bcrypt

def create_account():
    userName = input("Enter a username: ")
    password = getpass("Enter a password: ")
    firstName = input("Enter your first name: ").strip()
    lastName = input("Enter your last name: ").strip()
    roleLevel = "user"

    # Hash Password
    hashedPassword = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    connection = sqlite3.connect("MealManagement.db")
    cursor = connection.cursor()
    cursor.execute("""INSERT INTO Users (
                   username, password, first_name, last_name, role_level)
                   VALUES (?, ?, ?, ?, ?)""", (userName, hashedPassword, firstName, lastName, roleLevel)
                   )
    connection.commit()
    connection.close()
    print("Account created successfully!")