import random
import math
from os import urandom

class RSACipher:
    def __init__(self):
        self.private_key = None
        self.public_key = None
        self.n = None
        self.e = None
        self.d = None

    def generate_rsa_keys(self, key_size=256):
        def is_prime(n, k=5):
            if n < 2:
                return False
            for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]:
                if n % p == 0:
                    return n == p
            s, d = 0, n - 1
            while d % 2 == 0:
                s += 1
                d //= 2
            for _ in range(k):
                a = random.randint(2, min(n - 2, 1 << 20))
                x = pow(a, d, n)
                if x == 1 or x == n - 1:
                    continue
                for __ in range(s - 1):
                    x = pow(x, 2, n)
                    if x == n - 1:
                        break
                else:
                    return False
            return True

        def generate_prime(bits):
            while True:
                p = random.getrandbits(bits)
                p |= (1 << (bits - 1)) | 1
                if is_prime(p):
                    return p

        # Generate distinct primes
        p = generate_prime(key_size)
        q = generate_prime(key_size)
        while p == q:
            q = generate_prime(key_size)

        self.n = p * q
        phi = (p - 1) * (q - 1)

        self.e = 65537
        if math.gcd(self.e, phi) != 1:
            self.e = 3

        self.d = pow(self.e, -1, phi)

        # Store keys as strings
        self.public_key = f"{self.n},{self.e}"
        self.private_key = f"{self.n},{self.d}"
        return self.private_key, self.public_key

    def rsa_encrypt(self, plaintext, public_key=None):
        if public_key:
            try:
                n, e = map(int, public_key.split(','))
            except:
                raise ValueError("Invalid public key format")
        else:
            n, e = self.n, self.e

        if not n or not e:
            raise ValueError("Public key not initialized")

        # Calculate the modulus size in bytes
        modulus_bytes = (n.bit_length() + 7) // 8

        # Encode the plaintext to bytes
        plain_bytes = plaintext.encode('utf-8')

        # Check if the message is too long
        if len(plain_bytes) > modulus_bytes - 11:
            raise ValueError(f"Message too long (max {modulus_bytes - 11} bytes)")

        # Calculate padding length (PS length)
        ps_len = modulus_bytes - len(plain_bytes) - 3  # 3 bytes for 00 02 and 00

        # Ensure PS is at least 8 bytes
        if ps_len < 8:
            raise ValueError("Message too long for PKCS#1 v1.5 padding")

        # Generate non-zero random bytes for PS
        ps = bytearray()
        while len(ps) < ps_len:
            byte = urandom(1)[0]
            if byte != 0:
                ps.append(byte)

        # Construct the padded message: 00 || 02 || PS || 00 || M
        padded = b'\x00\x02' + ps + b'\x00' + plain_bytes

        # Convert to integer and encrypt
        message_int = int.from_bytes(padded, 'big')
        cipher_int = pow(message_int, e, n)
        return hex(cipher_int)[2:]

    def rsa_decrypt(self, ciphertext, private_key=None):
        """Decrypt and validate PKCS#1 v1.5 padding."""
        if private_key:
            try:
                n, d = map(int, private_key.split(','))
            except:
                raise ValueError("Invalid private key format")
        else:
            n, d = self.n, self.d

        if not n or not d:
            raise ValueError("Private key not initialized")

        # Convert hex to int
        try:
            cipher_int = int(ciphertext, 16)
        except:
            raise ValueError("Invalid ciphertext format")

        # Decrypt
        message_int = pow(cipher_int, d, n)
        byte_length = (n.bit_length() + 7) // 8
        padded = message_int.to_bytes(byte_length, 'big')

        # Validate padding
        if len(padded) < 11 or padded[0:2] != b'\x00\x02':
            raise ValueError("Decryption error: Invalid padding")
        try:
            sep = padded.index(b'\x00', 2)
        except ValueError:
            raise ValueError("Decryption error: Padding corrupt")
        return padded[sep+1:].decode('utf-8')