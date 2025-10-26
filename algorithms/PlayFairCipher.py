class PlayfairCipher:
    def __init__(self, key):
        key = key.lower().replace(" ", "").replace("j", "i")
        key_table = []
        for char in key:
            if char not in key_table and char.isalpha():
                key_table.append(char)
        for char in "abcdefghiklmnopqrstuvwxyz":
            if char not in key_table:
                key_table.append(char)
        self.key_table = [key_table[i:i + 5] for i in range(0, 25, 5)]

    def _find_position(self, char):
        char = char.lower().replace("j", "i")
        for i, row in enumerate(self.key_table):
            for j, c in enumerate(row):
                if c == char:
                    return (i, j)
        raise ValueError(f"Character '{char}' not found in the key table.")

    def _process_message(self, message):
        message = message.lower().replace(" ", "").replace("j", "i")
        processed = []
        i = 0
        while i < len(message):
            a = message[i]
            if i + 1 == len(message):
                processed.append(a + 'z')
                break
            b = message[i + 1]
            if a == b:
                processed.append(a + 'x')
                i += 1
            else:
                processed.append(a + b)
                i += 2
        # Join the list into a string and ensure even length
        processed_str = ''.join(processed)
        if len(processed_str) % 2 != 0:
            processed_str += 'z'
        return processed_str

    def _remove_padding(self, text):
        # Remove trailing 'z' added for padding
        if text.endswith('z'):
            text = text[:-1]
        # Remove 'x' between duplicate letters
        cleaned = []
        i = 0
        while i < len(text):
            if i + 1 < len(text) and text[i] == text[i + 1]:
                cleaned.append(text[i])
                i += 2  # Skip the 'x' added after duplicate
            else:
                cleaned.append(text[i])
                i += 1
        return ''.join(cleaned)

    def encrypt(self, message):
        processed = self._process_message(message)
        ciphertext = []
        for i in range(0, len(processed), 2):
            a, b = processed[i], processed[i + 1]
            row1, col1 = self._find_position(a)
            row2, col2 = self._find_position(b)
            if row1 == row2:
                ciphertext.append(self.key_table[row1][(col1 + 1) % 5])
                ciphertext.append(self.key_table[row2][(col2 + 1) % 5])
            elif col1 == col2:
                ciphertext.append(self.key_table[(row1 + 1) % 5][col1])
                ciphertext.append(self.key_table[(row2 + 1) % 5][col2])
            else:
                ciphertext.append(self.key_table[row1][col2])
                ciphertext.append(self.key_table[row2][col1])
        return ''.join(ciphertext)

    def decrypt(self, ciphertext):
        processed_ct = ciphertext.lower().replace(" ", "").replace("j", "i")
        decrypted = []
        for i in range(0, len(processed_ct), 2):
            a, b = processed_ct[i], processed_ct[i + 1]
            row1, col1 = self._find_position(a)
            row2, col2 = self._find_position(b)
            if row1 == row2:
                decrypted.append(self.key_table[row1][(col1 - 1) % 5])
                decrypted.append(self.key_table[row2][(col2 - 1) % 5])
            elif col1 == col2:
                decrypted.append(self.key_table[(row1 - 1) % 5][col1])
                decrypted.append(self.key_table[(row2 - 1) % 5][col2])
            else:
                decrypted.append(self.key_table[row1][col2])
                decrypted.append(self.key_table[row2][col1])
        decrypted_str = ''.join(decrypted)
        return decrypted_str