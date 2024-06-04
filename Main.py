import User
import sqlite3
from getpass import getpass
from Database import create_or_connect_db
import Consultant

def main():
    create_or_connect_db()
    Login()

def Login():
    response = input("Do you have an account? (y/n) ")
    if response == "y":
        username = input("Enter your username: ")
        password = getpass("Enter your password: ")

        connection = sqlite3.connect("MealManagement.db")
        cursor = connection.cursor()

        cursor.execute("SELECT username, password FROM Users WHERE username =?", (username,))
        user_data = cursor.fetchone()
        
        if user_data:
            if user_data[1] == password:
                print("Login succes")
            else:
                print("Fail")
        else:
            print("Users not found")
        connection.close()

    elif response == "n":
        User.create_account()
    else:
        print("Invalid input. Please try again.")
        Login()


if __name__ == "__main__":
    main()


    