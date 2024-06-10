# System admin
import sqlite3

def menu(username):
    
    connection = sqlite3.connect("MealManagement.db")
    cursor = connection.cursor()

    cursor.execute("SELECT username, password, role_level FROM Users WHERE username =?", (username))
    user_data = cursor.fetchone()

    role_level  = user_data[2]
    print(f"Welcome {username} ({role_level})")
    print("\n--- System Admin Menu ---")
    #Eigen gegevens
    #List van users

    #Add new consultant
    #Modify, update consultant
    #Delete consultant
    #Give consultant temp password

    #Backup, restore members info, users data

    #See logs

    #Add new member
    #Modify or update member
    #Delete member (consultant cant do that)
    #Search, retriev info of member

