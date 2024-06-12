#Super Admin
import sqlite3
import Main
import time
import pandas as pd
import User
from Validation import *
import bcrypt

# Hardcoded gegevens
super_username="super_admin"
super_password="Admin_123?"

def menu():
    
    connection = sqlite3.connect("MealManagement.db")
    cursor = connection.cursor()

    Main.clear()
    print(f"Welcome super admin!")
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
            Main.clear()
            consultant_menu()
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
    while True:
        Main.clear()
        print("\n--- List of users ---")
        # Login with current password
        cursor.execute("SELECT username, role_level FROM Users")
        user_data = cursor.fetchall()

        df = pd.DataFrame(user_data, columns=["Username", "Role"])
        df.index += 1
        df = df.rename_axis("ID")
        print(df)

        choice = input("\nGo back? (yes/no) ").strip().lower()
        if choice == "yes" or choice == "y":
            Main.clear()
            break
        else:
            print("Try again")
            continue
    connection.close()

#Consultant menu
def consultant_menu():
    connection = sqlite3.connect("MealManagement.db")
    cursor = connection.cursor()
    while True:
        Main.clear()
        print("\n--- Consultant menu ---")
        print("1. Make a new consultant")
        print("2. Make an user a consultant")
        print("3. Modify consultant")
        print("4. Delete a consultant")
        print("5. Reset password of a consultant")
        print("6. Go back")

        choice = input("Choose an option (1/2/3/4/5/6): ")
        
        if choice == "1":
            print("Make a new consultant")
            User.create_account(role="consultant")
            print("Added a new consultant")
            time.sleep(2)
        elif choice == "2":
            # Get information from user
            user_found = False
            while user_found == False:
                id = input("Enter user id: ").strip()

                choice = input("Go back? (yes/no)").strip().lower()
                if choice == "y":
                    break
                # Check if user exists in Users table
                user_cursor = cursor.execute(f"SELECT * FROM Users WHERE id = '{id}'")
                user = user_cursor.fetchone()
                if user is None:
                    print("User not found")
                else:
                    user_found = True
                    cursor.execute(f"UPDATE Users SET role_level = 'consultant' WHERE id = '{id}'")
                    
                    connection.commit()
                    connection.close()  
                    print("Changed succesfully")
                    time.sleep(2)
                break
        elif choice == "3":
            Main.clear()
            print("\n--- Update member ---")
            id_to_update = input("Enter the id of the user you want to update: ").strip()
            
            cursor.execute("SELECT * FROM Users WHERE id = ?", (id_to_update,))
            user = cursor.fetchall()

            choice = input("Go back? (yes/no) ").strip().lower()
            if choice == "yes" or choice == "y":
                break

            if user == []:
                Main.clear()
                print("User not found")
                time.sleep(2)
                continue
            else:
                print("""List of fields:
                      username
                      first_name
                      last_name
                      """)
                datatype_to_update = input("Enter the field you want to update: ").strip()

                if datatype_to_update == "username":
                    loop = True
                    while loop:
                        print(f"Username at the moment: {user[0][1]}")
                        username = input("Enter username: ").strip()
                        loop = validate_username(username)
                        # update member
                        if not loop:
                            cursor.execute("UPDATE users SET username = ? WHERE id = ?", (username, id_to_update))
                            connection.commit()
                            print("Username updated successfully")
                            time.sleep(2)
                            break
                elif datatype_to_update == "first_name":
                    loop = True
                    while loop:
                        first_name = input("Enter new first name: ").strip()
                        loop = validate_first_name(first_name)
                        # update member
                        if not loop:
                            cursor.execute("UPDATE Members SET first_name = ? WHERE id = ?", (first_name, id_to_update))
                            connection.commit()
                            print("First name updated successfully")
                            time.sleep(2)
                            break
                elif datatype_to_update == "last_name":
                    loop = True
                    while loop:
                        last_name = input("Enter last name: ").strip()
                        loop = validate_last_name(last_name)
                        # update member
                        if not loop:
                            cursor.execute("UPDATE Members SET last_name = ? WHERE id = ?", (last_name, id_to_update))
                            connection.commit()
                            print("Last name updated successfully")
                            time.sleep(2)
                            break
                else:
                    Main.clear()
                    print("Invalid input")
                    time.sleep(2)
                    continue
        elif choice == "4":
            Main.clear()
            print("\n--- Delete consultant ---")
            id_to_delete = input("Enter the id of the consultant you want to delete: ").strip()
            
            cursor.execute("SELECT * FROM Users WHERE id = ?", (id_to_delete,))
            user = cursor.fetchall()

            choice = input("Go back? (yes/no) ").strip().lower()
            if choice == "yes" or choice == "y":
                break

            if user == []:
                Main.clear()
                print("User not found")
                time.sleep(2)
                continue
            else:
                cursor.execute("DELETE FROM Users WHERE id = ?", (id_to_delete,))
                connection.commit()
                print("Consultant deleted successfully")
                time.sleep(2)
        elif choice == "5":
            Main.clear()
            print("\n--- Reset password of a consultant ---")
            pw_to_delete = input("Enter the id of the consultant for the password you want to delete: ").strip()

            cursor.execute("SELECT password FROM Users WHERE id = ?", (pw_to_delete,))
            user = cursor.fetchall()

            choice = input("Go back? (yes/no) ").strip().lower()
            if choice == "yes" or choice == "y":
                break

            if user == []:
                Main.clear()
                print("User not found")
                time.sleep(2)
                continue
            else:
                cursor.execute("UPDATE Users SET password = ? WHERE id = ?", (bcrypt.hashpw("Temp_123?".encode('utf-8'), bcrypt.gensalt()), pw_to_delete))
                connection.commit()
                print("Password reset successfully")
                time.sleep(2)
        elif choice == "6":
            break

# System admin menu
def systemadmin_menu():
    connection = sqlite3.connect("MealManagement.db")
    cursor = connection.cursor()
    while True:
        Main.clear()
        print("\n--- System admin menu ---")
        print("1. Make a new system admin")
        print("2. Make an user an admin")
        print("3. Modify admin")
        print("4. Delete a consultant")
        print("5. Reset password of a consultant")
        print("6. Go back")

        choice = input("Choose an option (1/2/3/4/5/6): ")