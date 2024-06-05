import sqlite3

Roles = ('admin', 'consultant', 'member', 'user')
Genders = ('Male', 'Female', 'Neither')
Cities = ('Papendrecht', 'Delft', 'Rotterdam', 'Den Haag', 'Schiedam', 'Zwolle', 'Leiden', 'Groningen', 'Maastricht', 'Urk')

def create_or_connect_db():
    connection = sqlite3.connect("MealManagement.db")

    cursor = connection.cursor()

    roles_str = str(Roles).replace('[', '(').replace(']', ')')
    genders_str = str(Genders).replace('[', '(').replace(']', ')')
    cities_str = str(Cities).replace('[', '(').replace(']', ')')
    
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS Users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    role_level TEXT NOT NULL CHECK(role_level IN {roles_str})
                )
                """)

    cursor.execute(f"""CREATE TABLE IF NOT EXISTS Members (
                    member_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    gender TEXT NOT NULL CHECK(gender IN {genders_str}),
                    weight DOUBLE NOT NULL,
                    street TEXT NOT NULL,
                    house_number INTEGER NOT NULL,
                    postal_code TEXT NOT NULL,
                    city TEXT NOT NULL CHECK(city IN {cities_str}),
                    country TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    phone_number TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES Users(id)
                    )""")

    connection.commit()
    connection.close()


