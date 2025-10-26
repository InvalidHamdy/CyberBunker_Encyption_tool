import sqlitecloud
from algorithms.SHA_256 import sha_256
import os
from dotenv import load_dotenv

class LoginHandler:
    def __init__(self):
        load_dotenv()
        self.connection_string = os.getenv("CONNECTION_STRING")

    def __enter__(self):
        self.conn = sqlitecloud.connect(self.connection_string)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()

    def validate_user(self, email: str, password: str) -> bool:
        try:
            hashed_password = sha_256(password.encode('utf-8')).hex()
            cursor = self.conn.cursor()
            query = "SELECT COUNT(*) FROM USERS WHERE EMAIL = ? AND PASSWORD = ?"
            cursor.execute(query, (email, hashed_password))
            result = cursor.fetchone()
            cursor.close()  # Manually close the cursor
            return result[0] > 0 if result else False
        except sqlitecloud.Error as err:
            print(f"Database error: {err}")
            return False
        except Exception as e:
            print(f"Validation error: {e}")
            return False
    def getUserName(self,email: str) -> str:
        cursor = self.conn.cursor()
        query = "SELECT USERNAME FROM USERS WHERE EMAIL = ?"
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        cursor.close()
        return result[0] if result else None