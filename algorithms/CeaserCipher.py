class CaesarCipher:  # Fixed typo in class name (Ceaser -> Caesar)
    def __init__(self, key):
        self.key = key % 26

    def encrypt(self, text):
        result = ""
        for char in text:
            if char.isupper():
                result += chr((ord(char) + self.key - 65) % 26 + 65)
            elif char.islower():
                result += chr((ord(char) + self.key - 97) % 26 + 97)
            else:
                result += char  # Keep non-alphabetic characters unchanged
        return result

    def decrypt(self, text):
        cipher = CaesarCipher(-self.key)
        return cipher.encrypt(text)

