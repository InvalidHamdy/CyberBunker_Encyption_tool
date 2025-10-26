import random
import time

class OTPHandler:
    def __init__(self, length=6, expiry_seconds=300):
        self.length = length
        self.expiry = expiry_seconds
        self.current_otp = None
        self.generation_time = None

    def create_otp(self):
        self.current_otp = ''.join(str(random.randint(0, 9)) for _ in range(self.length))
        self.generation_time = time.time()
        return self.current_otp

    def confirm_otp(self, otp):
        if not self.current_otp or not otp:
            return False
        return (otp == self.current_otp and
                (time.time() - self.generation_time) <= self.expiry)

