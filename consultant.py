import sqlite3

from getpass import getpass
import bcrypt

import main
import time

from safe_data import *
from super_admin import *

# logging
from log_config import logmanager as log_manager
log_instance = log_manager()

# MENU.

def menu(username):
    main.clear()
    connection = sqlite3.connect("mealmanagement.db")
    cursor = connection.cursor()

    cursor.execute("SELECT username, password FROM Users WHERE username = ?", (username,))
    user_data = cursor.fetchone()

    while True:
        main.clear()
        print("\n--- Consultant Menu ---")
        print(f"--Welcome {username}--\n")

        print("1. Update password")
        print("2. Members menu")
        print("3. Logout")
        choice = input("Choose an option (1/2/3): ").strip()

        if choice == "1":
            main.clear()
            update_password(username)
        elif choice == "2":
            main.clear()
            print("\n--- Members Menu (from consultant) ---")

            print("1. Process member request")
            print("2. Modify member")
            print("3. Delete member")
            print("4. Go back")
            choice = input("Choose an option (1/2/3/4): ").strip()

            if choice == "1":
                main.clear()
                add_member(username)
            elif choice == "2":
                main.clear()
                modify_user("member", username)
            elif choice == "3":
                main.clear()
                delete_user("member", username)
            elif choice == "4":
                continue
            else:
                main.clear()
                log_instance.log_activity(f"{username}", "System", "Invalid input in the main menu", "No")
                time.sleep(2)
        elif choice == "3":
            print("You logged out, Goodbye!")
            log_instance.log_activity(f"{username}", "System", "Logged out", "No")
            break
        else:
            log_instance.log_activity(f"{username}", "System", "Invalid input in the main menu", "No")

# ACTIONS

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
            log_instance.log_activity(username, "Update password", "Nonexistent consultant tried to update password", "Yes")
            exit()
            
    # Check if password is correct
    input_password = getpass("Enter your current password: ")
    if not bcrypt.checkpw(input_password.encode('utf-8'), found_password):
        log_instance.log_activity(username, "Update password", "Incorrect password", "No")
        return False
    else:
        while True:
            main.clear()
            print("\n--- Update Password ---")
            new_password = getpass("Enter your new password: ")
            if (new_password == input_password):
                main.clear()
                print("Invalid password")
                log_instance.log_activity(username, "Update password", "Entered same password as the old password", "No")
                time.sleep(2)
                continue
            elif (not validate_password(new_password)):
                main.clear()
                print("Invalid password")
                log_instance.log_activity(username, "Update password", "Invalid password", "No")
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
                log_instance.log_activity(username, "Update password", f"Password updated successfully for user: '{username}'", "No")
                time.sleep(2)
                break
        return True
