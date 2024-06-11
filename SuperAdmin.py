#Super Admin
import sqlite3
import Main
import pandas as pd

# Hardcoded gegevens
super_username="super_admin"
super_password="Admin_123?"

def menu():
    
    connection = sqlite3.connect("MealManagement.db")
    cursor = connection.cursor()

    # cursor.execute("SELECT username, password, role_level FROM Users WHERE username =?", (username))
    # user_data = cursor.fetchone()

    # role_level  = user_data[2]
    print(f"Welcome super admin!)")
    print("\n--- Super Admin Menu ---")
    #List van users
    while True:

    #List van users
        print("1. List of users")
    #Add new consultant
    #Modify, update consultant
    #Delete consultant
    #Give consultant temp password
        print("2. Consultant menu")
    #Define/Add new system admin
    #Modify, update admin
    #Delete admin
    #Give admin temp password
        print("3. System admin menu")
    #Backup, restore members info, users data
    #See logs
        print("4. System")
    #Add new member
    #Modify or update member
    #Delete member (consultant cant do that)
    # Delete member
    #Search, retriev info of member
        print("5. Member menu")

        choice = input("Choose an option (1/2/3/4/5): ").strip()

        if choice == "1":
            Main.clear()
            list_users()
        elif choice == "2":
            break
        elif choice == "3":
            break
        elif choice == "4":
            break
        elif choice == "5":
            break
        else:
            print("Invalid input")
            connection.close()


def list_users():
    connection = sqlite3.connect("MealManagement.db")
    cursor = connection.cursor()
    Main.clear()
    print("\n--- List of users ---")
    # Login with current password
    cursor.execute("SELECT username, role_level FROM Users")
    user_data = cursor.fetchall()

    df = pd.DataFrame(user_data, columns=["Username", "Role"])
    print(df)

    while True:
        print("\n1. Go back")
        print("2. Exit")
        choice = input("Choose an option: ").split()

        if choice == "1":
            break
        elif choice == "2":
            print("Exiting the program. Goodbye!")
            exit()
        else:
            print("Try again")

    connection.close()
