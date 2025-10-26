class VigenereCipher:
    def __init__(self, key):
        if not key.isalpha():
            raise ValueError("Key must contain letters only.")
        self.key = key.lower()

    def _shift_char(self, char, key_char, decrypt=False):
        shift = ord(key_char) - ord('a')
        if decrypt:
            shift = -shift

        base = ord('A') if char.isupper() else ord('a')
        return chr((ord(char) - base + shift) % 26 + base)

    def _transform(self, text, decrypt=False):
        result = ''
        key_length = len(self.key)
        key_index = 0

        for char in text:
            if char.isalpha():
                key_char = self.key[key_index % key_length]
                result += self._shift_char(char, key_char, decrypt)
                key_index += 1
            else:
                result += char

        return result

    def encrypt(self, text):
        return self._transform(text, decrypt=False)

    def decrypt(self, text):
        return self._transform(text, decrypt=True)