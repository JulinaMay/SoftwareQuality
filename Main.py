import User
import sqlite3
from getpass import getpass
from Database import create_or_connect_db
import Consultant
from os import system, name

def main():
    create_or_connect_db()
    clear()
    Login()
    Consultant.proces_member_request()

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

def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux
    else:
        _ = system('clear')
    
if __name__ == "__main__":
    main()
