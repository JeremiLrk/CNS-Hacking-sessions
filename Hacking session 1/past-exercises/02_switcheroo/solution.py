"""SWITCHEROO — monoalphabetic substitution.

WHEN TO TRY: You are given one mapping for plain letters and another for
cipher letters. Every letter has its own replacement.

Very important: to DECRYPT, find where a ciphertext letter appears in the
cipher alphabet, then look at the SAME position in the plain alphabet.
"""

PLAIN_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
CIPHER_ALPHABET = "QWERTYUIOPASDFGHJKLZXCVBNM"
CIPHERTEXT = "EFL{STZZTK-LGXH}"


def decrypt_substitution(ciphertext, plain_alphabet, cipher_alphabet):
    if len(plain_alphabet) != len(cipher_alphabet):
        raise ValueError("The two alphabets must have the same length")

    if len(set(cipher_alphabet)) != len(cipher_alphabet):
        raise ValueError("Cipher alphabet has duplicate letters")

    result = ""

    for letter in ciphertext:
        if letter in cipher_alphabet:
            position = cipher_alphabet.index(letter)
            result += plain_alphabet[position]
        else:
            result += letter

    return result


if __name__ == "__main__":
    print(decrypt_substitution(CIPHERTEXT, PLAIN_ALPHABET, CIPHER_ALPHABET))
