from db import get_db_connection

class User:
    @staticmethod
    def create_user(name, email, password, role, carDetails=None, license=None):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO Users (name, email, password, role, carDetails, license)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, email, password, role, carDetails, license))
        connection.commit()
        cursor.close()
        connection.close()

    @staticmethod
    def get_all_users():
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Users")
        users = cursor.fetchall()
        cursor.close()
        connection.close()
        return users
