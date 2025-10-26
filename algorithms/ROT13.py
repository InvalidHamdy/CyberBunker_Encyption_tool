class ROT13:
    #dic for upper_letters
    _UPPER_MAP = {chr(i): chr((i - 65 + 13) % 26 + 65) for i in range(65, 91)}
    # dic for lower_letters
    _LOWER_MAP = {chr(i): chr((i - 97 + 13) % 26 + 97) for i in range(97, 123)}

    def encrypt(self, message: str) -> str:
        encrypted = []
        for char in message:
            if char in self._UPPER_MAP:
                encrypted.append(self._UPPER_MAP[char])
            elif char in self._LOWER_MAP:
                encrypted.append(self._LOWER_MAP[char])
            else:
                encrypted.append(char)
        return ''.join(encrypted)

    def decrypt(self, message: str) -> str:
        return self.encrypt(message)