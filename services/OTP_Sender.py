import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import os
from dotenv import load_dotenv
class OTPSender:
    def __init__(self, otp_handler):
        self.otp_handler = otp_handler
        load_dotenv()  # Load environment variables
        self.sender_email = os.getenv("EMAIL_ADDRESS")
        self.sender_password = os.getenv("EMAIL_PASSWORD") # Replace with your app password

    def send_otp_email(self, recipient_email):
        otp = self.otp_handler.create_otp()
        msg = MIMEText(f"Your OTP is: {otp}\nValid for 5 minutes")
        msg['Subject'] = 'Cyber Bunker Verification Code'
        msg['From'] = formataddr(('Cyber Bunker', self.sender_email))
        msg['To'] = recipient_email

        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, [recipient_email], msg.as_string())
            return True
        except Exception as e:
            print(f"Email error: {str(e)}")
            return False