import CeaserCipher

def test_caesar_cipher():
    cipher = CeaserCipher(4)

    # Test encryption
    assert cipher.encrypt("ATTACKATONCE") == "EXXEGOEXSRGI", "Encryption failed for ATTACKATONCE"
    assert cipher.encrypt("Hello123!") == "Lipps123!", "Encryption failed for Hello123!"

    # Test decryption
    assert cipher.decrypt("EXXEGOEXSRGI") == "ATTACKATONCE", "Decryption failed for EXXEGOEXSRGI"
    assert cipher.decrypt("Lipps123!") == "Hello123!", "Decryption failed for Lipps123!"

    print("All tests passed!")


if __name__ == "__main__":
    test_caesar_cipher()