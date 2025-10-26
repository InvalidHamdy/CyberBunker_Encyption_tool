LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

class Substitiotion:
    def __init__(self, key):
        # Validate the key
        if len(key) != 26 or not key.isalpha() or len(set(key.upper())) != 26:
            raise ValueError("Key must be 26 unique uppercase letters (A-Z).")
        self.key = key.upper()  # Force uppercase

    def encrypt(self, message):
        translated = ''
        for symbol in message:
            if symbol.upper() in LETTERS:
                sym_index = LETTERS.find(symbol.upper())
                translated += self.key[sym_index]
            else:
                translated += symbol  # Non-alphabetic characters remain unchanged
        return translated

    def decrypt(self, message):
        translated = ''
        for symbol in message:
            if symbol.upper() in self.key:
                sym_index = self.key.find(symbol.upper())
                translated += LETTERS[sym_index]
            else:
                translated += symbol
        return translated