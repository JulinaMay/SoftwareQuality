import sqlite3

def create_or_connect_db():
    connection = sqlite3.connect("MealManagement.db")

    cursor = connection.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS Users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    role_level TEXT NOT NULL CHECK(role_level IN('admin','consultant','member','user'))
                )
                """)

    Cities = "('Papendrecht', 'Delft', 'Rotterdam', 'Den Haag', 'Schiedam', 'Zwolle', 'Leiden', 'Groningen', 'Maastricht', 'Urk')"

    cursor.execute(f"""CREATE TABLE IF NOT EXISTS Members (
                    member_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    gender TEXT NOT NULL CHECK(gender IN('Female', 'Male', 'Neither')),
                    weight DOUBLE NOT NULL,
                    street TEXT NOT NULL,
                    house_number INTEGER NOT NULL,
                    postal_code TEXT NOT NULL,
                    city TEXT NOT NULL CHECK(city IN {Cities}),
                    country TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    phone_number TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES Users(id)
                    )""")

    connection.commit()
    connection.close()


