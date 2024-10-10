# System admin.
import sqlite3

from getpass import getpass
import bcrypt

import time

import main
from super_admin import *

# logging
from log_config import *

def menu(username):
    main.clear()
    connection = sqlite3.connect("mealmanagement.db")
    cursor = connection.cursor()

    cursor.execute("SELECT username, password, role_level FROM Users WHERE username =?", (username,))
    user_data = cursor.fetchone()

    while True:
        print(f"Welcome {username}")
        print("\n--- System Admin Menu ---")

    #Eigen gegevens
        print("1. Update password")
    #List van users
        print("2. List of users")
    #Add new consultant
    #Modify, update consultant
    #Delete consultant
    #Give consultant temp password
        print("3. Consultant menu")
    #Backup, restore members info, users data
    #See logs
        print("4. System")
    #Add new member
    #Modify or update member
    #Delete member (consultant cant do that)
    # Delete member
    #Search, retriev info of member
        print("5. Member menu")
    # logout
        print("6. Logout")

        choice = input("Choose an option (1/2/3/4/5/6): ").strip()

        if choice == "1":
            main.clear()
            update_password(username)
        elif choice == "2":
            main.clear()
            list_users()
        elif choice == "3":
            main.clear()
            consultant_menu()
        elif choice == "4":
            system_menu()
        elif choice == "5":
            main.clear()    
            Main()
        elif choice == "6":
            print("You logged out, Goodbye!")
            log_activity(username, "System", "Program exited", "No")
            break
        else:
            main.clear()
            log_activity(username, "System", "Invalid input at the modifying menu", "No")
            time.sleep(2)

# Functies
def update_password(username): # TODO: Add validation
    connection = sqlite3.connect("mealmanagement.db")
    cursor = connection.cursor()

    main.clear()
    print("\n--- Update Password ---")
    # Login with current password
    cursor.execute("SELECT * FROM Users")
    user_data = cursor.fetchall()
    decrypted_username = ""
    found_password = ""
    for i in range(len(user_data)):
        decrypted_username = decrypt_data(private_key(), user_data[i][1])
        if decrypted_username == username:
            found_password = user_data[i][2]
            break

        # check if have reached end of loop
        if i == len(user_data) - 1:
            print("User not found")
            log_activity(username, "Update password" "Nonexistent consultant tried to update password", "Yes")
            exit()
            
    # Check if password is correct
    input_password = getpass("Enter your current password: ")
    if not bcrypt.checkpw(input_password.encode('utf-8'), found_password):
        log_activity(username, "Update password" "Incorrect password", "No")
        return False
    else:
        while True:
            main.clear()
            print("\n--- Update Password ---")
            new_password = getpass("Enter your new password: ")
            if (new_password == input_password):
                main.clear()
                print("New password can't be the same as the old password")
                log_activity(username, "Update password", "Entered same password as the old password", "No")
                time.sleep(2)
                continue
            elif (not validate_password(new_password)):
                main.clear()
                print("Invalid password")
                log_activity(username, "Update password", "Invalid password", "No")
                time.sleep(2)
                continue
            else:
                # enter password in database
                hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

                # Hier gaat het fout, je moet de username encrypten voordat je het in de database opzoekt
                cursor.execute("SELECT * FROM Users")
                user_data = cursor.fetchall()
                decrypted_username = ""
                for i in range(len(user_data)):
                    decrypted_username = decrypt_data(private_key(), user_data[i][1])
                    if decrypted_username == username:
                        encrypted_username = user_data[i][1]
                        break

                cursor.execute("UPDATE Users SET password = ? WHERE username = ?", (hashed_password, encrypted_username))

                connection.commit()
                connection.close()
                main.clear()
                print("Password updated successfully")
                log_activity(username, "Update password" f"Password updated successfully for user: '{username}'", "No")
                time.sleep(2)
                break
        return True


