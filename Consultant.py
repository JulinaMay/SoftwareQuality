import sqlite3

def proces_member_request():
    connection = sqlite3.connect("MealManagement.db")
    cursor = connection.cursor()

    # Get information from user
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    age = int(input("Enter age: "))
    gender = input("Enter Gender: ")
    weight = float(input("Enter weight: "))
    street = input("Enter street: ")
    house_number = int(input("Enter house number: "))
    postal_code = input("Enter postal code: ")
    city = input("Enter city: ")
    country = input("Enter country: ")
    email = input("Enter email: ")
    phone_number = input("Enter phone number: ")
        
    # Get user_id from Users table
    user = cursor.execute(f"SELECT * FROM Users WHERE first_name = {first_name} AND last_name = {last_name}")
    user_id = user.fetchone()[0]

    cursor.execute(f"INSERT INTO Members (user_id, first_name, last_name, age, gender, weight, street, house_number, postal_code, city, country, email, phone_number) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (user_id, first_name, last_name, age, gender, weight, street, house_number, postal_code, city, country, email, phone_number))


    connection.commit()
    connection.close()

