"""THE FRENCH CIPHER — Vigenere with a repeating keyword.

WHEN TO TRY: A sentence says a keyword is used to encrypt letters with
shifts, and the same word repeats again and again.

The hint says a French crescent-shaped pastry: the KEY is 'croissant'.
Do NOT advance the key on braces or dashes; they are not encrypted letters.
"""

CIPHERTEXT = "eeg{kjgiflceha-sje-oxvksz-lzaa-ikqni}"
KEY = "croissant"


def decrypt_vigenere(ciphertext, key):
    key = key.lower()
    if not key or not key.isalpha():
        raise ValueError("Key must be alphabetic and not empty")

    result = ""
    key_position = 0

    for letter in ciphertext:
        if "a" <= letter <= "z":
            # Find the number of the encrypted letter: a=0, b=1, etc.
            encrypted_number = ord(letter) - ord("a")

            # Get the next letter of our repeating keyword.
            current_key_letter = key[key_position % len(key)]
            shift = ord(current_key_letter) - ord("a")

            # Undo the addition used when encrypting.
            original_number = (encrypted_number - shift) % 26
            result += chr(original_number + ord("a"))
            key_position += 1
        else:
            result += letter

    return result


if __name__ == "__main__":
    print(decrypt_vigenere(CIPHERTEXT, KEY))
