import sqlitecloud
from algorithms.SHA_256 import sha_256
from services.OTP_Gen import OTPHandler
from services.OTP_Sender import OTPSender
import re
from dotenv import load_dotenv
import os

class SignUpHandler:
    def __init__(self):
        load_dotenv()
        self.connection_string = os.getenv("CONNECTION_STRING")
        self.otp_handler = OTPHandler()
        self.otp_sender = OTPSender(self.otp_handler)

    def validate_inputs(self, first_name, last_name, username, email, password, confirm_password):
        if not all([first_name, last_name, username, email, password, confirm_password]):
            return False, "All fields are required"
        if password != confirm_password:
            return False, "Passwords don't match"
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return False, "Invalid email format"
        return True, ""

    def email_exists(self, email):
        try:
            conn = sqlitecloud.connect(self.connection_string)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM USERS WHERE EMAIL = ?", (email,))
            result = cursor.fetchone()[0]
            conn.close()
            return result > 0
        except sqlitecloud.Error as err:
            print(f"Database error: {err}")
            return False

    def insert_user(self, first_name, last_name, username, email, password):
        hashed_password = sha_256(password.encode()).hex()
        try:
            conn = sqlitecloud.connect(self.connection_string)
            cursor = conn.cursor()
            query = "INSERT INTO USERS (FIRST_NAME, LAST_NAME, USERNAME, EMAIL, PASSWORD) VALUES (?, ?, ?, ?, ?)"
            cursor.execute(query, (first_name, last_name, username, email, hashed_password))
            conn.commit()
            conn.close()
            return True
        except sqlitecloud.Error as err:
            print(f"Database error: {err}")
            return False

    def process_signup(self, first_name, last_name, username, email, password, confirm_password, otp):
        if not self.otp_handler.confirm_otp(otp):
            return False, "Invalid or expired OTP"
        valid, message = self.validate_inputs(first_name, last_name, username, email, password, confirm_password)
        if not valid:
            return False, message
        if self.email_exists(email):
            return False, "Email already registered"
        if self.insert_user(first_name, last_name, username, email, password):
            return True, "Registration successful"
        return False, "Registration failed"