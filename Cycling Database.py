
"""
in this file i am tasked with creating a database using mysql

Table1 (Walking/running)
User, Initial distance, Final distance, Time ,Initial Location ,Final Location,Rewards Issued

 Table2 ( Carpooling )
 User, Initial distance, Final distance, Time ,Initial Location ,Final Location,Rewards Issued,no_
"""
import mysql.connector
from mysql.connector import Error


# Database connection
def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='npol',
            database='Basic_db'
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection


# Create tables
def create_tables(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            total_distance FLOAT DEFAULT 0
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Friends (
            user_id INT,
            friend_id INT,
            PRIMARY KEY (user_id, friend_id),
            FOREIGN KEY (user_id) REFERENCES Users(user_id),
            FOREIGN KEY (friend_id) REFERENCES Users(user_id)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS CarpoolTrips (
            trip_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            friend_id INT,
            distance FLOAT NOT NULL,
            trip_date DATE NOT NULL,
            FOREIGN KEY (user_id) REFERENCES Users(user_id),
            FOREIGN KEY (friend_id) REFERENCES Users(user_id)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Rewards (
            reward_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            reward_points INT NOT NULL,
            reward_date DATE NOT NULL,
            FOREIGN KEY (user_id) REFERENCES Users(user_id)
        )
        """)

        connection.commit()
        print("Tables created successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


# Add a new user
def add_user(connection, name, email):
    cursor = connection.cursor()
    try:
        cursor.execute("""
        INSERT INTO Users (name, email) VALUES (%s, %s)
        """, (name, email))
        connection.commit()
        print("User added successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


# Add a friend relationship
def add_friend(connection, user_id, friend_id):
    cursor = connection.cursor()
    try:
        cursor.execute("""
        INSERT INTO Friends (user_id, friend_id) VALUES (%s, %s)
        """, (user_id, friend_id))
        connection.commit()
        print("Friend added successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


# Record a carpool trip
def record_trip(connection, user_id, friend_id, distance, trip_date):
    cursor = connection.cursor()
    try:
        cursor.execute("""
        INSERT INTO CarpoolTrips (user_id, friend_id, distance, trip_date) VALUES (%s, %s, %s, %s)
        """, (user_id, friend_id, distance, trip_date))

        # Update total distance for both users
        cursor.execute("""
        UPDATE Users SET total_distance = total_distance + %s WHERE user_id = %s
        """, (distance, user_id))

        cursor.execute("""
        UPDATE Users SET total_distance = total_distance + %s WHERE user_id = %s
        """, (distance, friend_id))

        connection.commit()
        print("Trip recorded successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


# Issue rewards based on distance
def issue_rewards(connection):
    cursor = connection.cursor()
    try:
        # Calculate rewards based on total distance
        cursor.execute("""
        SELECT user_id, total_distance FROM Users
        """)
        users = cursor.fetchall()

        for user in users:
            user_id, total_distance = user
            reward_points = int(total_distance // 10)  # 1 point per 10 km

            if reward_points > 0:
                cursor.execute("""
                INSERT INTO Rewards (user_id, reward_points, reward_date) VALUES (%s, %s, CURDATE())
                """, (user_id, reward_points))

        connection.commit()
        print("Rewards issued successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


# Main function
def main():
    connection = create_connection()
    if connection:
        create_tables(connection)

        # Example usage
        add_user(connection, "John Doe", "john@example.com")
        add_user(connection, "Jane Doe", "jane@example.com")
        add_friend(connection, 1, 2)
        record_trip(connection, 1, 2, 50.5, '2023-10-01')
        issue_rewards(connection)

        connection.close()


if __name__ == "__main__":
    main()
