class RailFenceCipher:
    def __init__(self):
        pass

    def encrypt(self, plaintext, key):
        """Encrypts plaintext using Rail Fence cipher"""
        try:
            key = int(key)
            if key <= 1:
                return plaintext
            rail = [''] * key
            row, step = 0, 1
            for char in plaintext:
                rail[row] += char
                if row == 0:
                    step = 1
                elif row == key - 1:
                    step = -1
                row += step
            return ''.join(rail)
        except Exception as e:
            raise Exception(f"Encryption error Rail Fence: {str(e)}")

    def decrypt(self, ciphertext, key):
        """Decrypts ciphertext using Rail Fence cipher"""
        try:
            key = int(key)
            if key <= 1:
                return ciphertext
            length = len(ciphertext)
            rail = [['\n' for _ in range(length)] for _ in range(key)]
            pos = 0
            row, step = 0, 1
            for _ in range(length):
                rail[row][pos] = '*'
                if row == 0:
                    step = 1
                elif row == key - 1:
                    step = -1
                row += step
                pos += 1
            index = 0
            for i in range(key):
                for j in range(length):
                    if rail[i][j] == '*' and index < length:
                        rail[i][j] = ciphertext[index]
                        index += 1
            result = []
            row, pos = 0, 0
            for _ in range(length):
                result.append(rail[row][pos])
                pos += 1
                if row == 0:
                    step = 1
                elif row == key - 1:
                    step = -1
                row += step
            return ''.join(result)
        except Exception as e:
            raise Exception(f"Decoding error Rail Fence: {str(e)}")