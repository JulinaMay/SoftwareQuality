import sqlite3
# import bcrypt

def create_account():
    userName = input("Enter a username: ")
    password = input("Enter a password: ")
    firstName = input("Enter your first name: ").strip()
    lastName = input("Enter your last name: ").strip()
    roleLevel = "user"

    # Hash Password

    connection = sqlite3.connect("MealManagement.db")
    cursor = connection.cursor()
    cursor.execute("""INSERT INTO Users (
                   username, password, first_name, last_name, role_level)
                   VALUES (?, ?, ?, ?, ?)""", (userName, password, firstName, lastName, roleLevel)
                   )
    connection.commit()
    connection.close()