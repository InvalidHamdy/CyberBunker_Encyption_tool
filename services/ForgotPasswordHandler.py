import re

import sqlitecloud
from algorithms.SHA_256 import sha_256
import os
from dotenv import load_dotenv
from services.OTP_Sender import OTPSender
from services.OTP_Gen import OTPHandler
class ForgotPasswordHandler:
    def __init__(self):
        load_dotenv()
        self.connection_string = os.getenv('CONNECTION_STRING')
        self.otp_handler = OTPHandler()
        self.otp_sender = OTPSender(self.otp_handler)

    def __enter__(self):
        self.conn = sqlitecloud.connect(self.connection_string)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()

    def validateMatchingPassword(self, password,confirmPassword):
        if(password == confirmPassword):
            return True
        else:
            return False

    def validate_password_constraints(self, password):
        # Check if password is at least 8 characters long
        if len(password) < 8:
            return False
        # Check for at least 1 digit
        if not re.search(r'\d', password):
            return False
        # Check for at least 1 special character
        if not re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:",.<>?/]', password):
            return False
        return True

    def updatePassword(self,userOtp,email,password,confirmPassword):
        hashed_password = sha_256(password.encode()).hex()
        if not self.otp_handler.confirm_otp(userOtp):
            return False
        if not self.validateMatchingPassword(password,confirmPassword):
            return False
        if not self.otp_handler.confirm_otp(userOtp):
            return False
        try:
                conn = sqlitecloud.connect(self.connection_string)
                cursor = conn.cursor()
                query = "UPDATE USERS SET PASSWORD = ? WHERE EMAIL = ?;"
                cursor.execute(query, (hashed_password, email))
                conn.commit()
                conn.close()
                return True
        except sqlitecloud.Error as e:
            print(f"Database error: {e}")
            return False
