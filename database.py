import sqlite3

# logging.
from log_config import logger

Roles = ('admin', 'consultant', 'member', 'user')
Genders = ('Male', 'Female', 'Neither')
Cities = ('Papendrecht', 'Delft', 'Rotterdam', 'Den Haag', 'Schiedam', 'Zwolle', 'Leiden', 'Groningen', 'Maastricht', 'Urk')

def create_or_connect_db():
    connection = sqlite3.connect("mealmanagement.db")

    cursor = connection.cursor()

    roles_str = str(Roles).replace('[', '(').replace(']', ')')
    genders_str = str(Genders).replace('[', '(').replace(']', ')')
    cities_str = str(Cities).replace('[', '(').replace(']', ')')
    
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS Users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    role_level TEXT NOT NULL CHECK(role_level IN {roles_str})
                )
                """)

    cursor.execute(f"""CREATE TABLE IF NOT EXISTS Members (
                        member_id TEXT PRIMARY KEY,
                        user_id INTEGER,
                        first_name TEXT NOT NULL,
                        last_name TEXT NOT NULL,
                        age TEXT NOT NULL,
                        gender TEXT NOT NULL,
                        weight TEXT NOT NULL,
                        street TEXT NOT NULL,
                        house_number TEXT NOT NULL,
                        postal_code TEXT NOT NULL,
                        city TEXT NOT NULL,
                        country TEXT NOT NULL,
                        email TEXT NOT NULL,
                        phone_number TEXT NOT NULL,
                        FOREIGN KEY (user_id) REFERENCES Users(id)
                    )""")

    connection.commit()
    connection.close()

def clear_database():
    connection = sqlite3.connect("mealmanagement.db")
    cursor = connection.cursor()

    cursor.execute("DROP TABLE IF EXISTS Users")
    cursor.execute("DROP TABLE IF EXISTS Members")

    connection.commit()
    connection.close()
