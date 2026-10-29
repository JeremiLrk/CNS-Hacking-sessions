"""TEST CHALLENGE — Caesar cipher.

WHEN TO TRY: Letters seem shifted by a fixed number in the alphabet.
Caesar has only 26 possible shifts, so test ALL of them.
"""

CIPHERTEXT = "fqv{iluvw-fkdoohqjh}"


def decrypt_caesar(ciphertext, shift):
    answer = ""

    for letter in ciphertext:
        if "a" <= letter <= "z":
            # A becomes 0, B becomes 1, ..., Z becomes 25.
            position = ord(letter) - ord("a")
            old_position = (position - shift) % 26
            answer += chr(old_position + ord("a"))
        elif "A" <= letter <= "Z":
            position = ord(letter) - ord("A")
            old_position = (position - shift) % 26
            answer += chr(old_position + ord("A"))
        else:
            # Braces and hyphens are not encrypted.
            answer += letter

    return answer


def main():
    for shift in range(26):
        print(f"Shift {shift:2}: {decrypt_caesar(CIPHERTEXT, shift)}")


if __name__ == "__main__":
    main()
