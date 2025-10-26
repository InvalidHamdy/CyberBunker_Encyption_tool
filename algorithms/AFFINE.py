def egcd(a, b):
    x, y, u, v = 0, 1, 1, 0
    while a != 0:
        q, r = b // a, b % a
        m, n = x - u * q, y - v * q
        b, a, x, y, u, v = a, r, u, v, m, n
    gcd = b
    return gcd, x, y


def modinv(a, m):
    gcd, x, y = egcd(a, m)
    if gcd != 1:
        return None  # modular inverse doesn't exist
    else:
        return x % m


class AffineCipher:
    def __init__(self, key_a, key_b):

        self.key_a = key_a
        self.key_b = key_b

        # Immediate key validation
        if not isinstance(key_a, int) or not isinstance(key_b, int):
            raise ValueError("Both keys must be integers")
        if modinv(key_a, 26) is None:
            raise ValueError("Key A must be coprime with 26")

    def encrypt(self, text):
        """Encrypts text using Affine cipher C = (a*P + b) % 26"""
        encrypted = []
        for char in text:
            if char.isupper():
                p = ord(char) - ord('A')
                c = (self.key_a * p + self.key_b) % 26
                encrypted.append(chr(c + ord('A')))
            elif char.islower():
                p = ord(char) - ord('a')
                c = (self.key_a * p + self.key_b) % 26
                encrypted.append(chr(c + ord('a')))
            else:
                encrypted.append(char)  # Preserve non-alphabetic chars
        return ''.join(encrypted)

    def decrypt(self, cipher):
        """Decrypts Affine cipher text P = (a^-1 * (C - b)) % 26"""
        decrypted = []
        a_inv = modinv(self.key_a, 26)
        if a_inv is None:
            raise ValueError("No modular inverse exists for key A")

        for char in cipher:
            if char.isupper():
                c = ord(char) - ord('A')
                p = (a_inv * (c - self.key_b)) % 26
                decrypted.append(chr(p + ord('A')))
            elif char.islower():
                c = ord(char) - ord('a')
                p = (a_inv * (c - self.key_b)) % 26
                decrypted.append(chr(p + ord('a')))
            else:
                decrypted.append(char)
        return ''.join(decrypted)