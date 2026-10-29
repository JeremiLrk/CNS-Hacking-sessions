"""[COURSE Part 2] Old-school ciphers: Caesar, frequency, Vigenere.

WHEN:
- Ciphertext looks like mostly letters A-Z, not random-looking bytes.
- Caesar: every letter shifted by same amount; try 26 possibilities.
- Vigenere: key is a repeating word; different positions use different shifts.
- Substitution: use frequency analysis and word patterns.
"""
from collections import Counter
import string


def caesar(text, shift):
    answer = ""
    for char in text:
        if char.isascii() and char.isalpha():
            start = ord("A") if char.isupper() else ord("a")
            position = ord(char) - start
            shifted = (position + shift) % 26
            answer += chr(start + shifted)
        else:
            answer += char
    return answer


def try_all_caesar(ciphertext):
    for shift in range(26):
        print("Key", shift, "->", caesar(ciphertext, -shift))


def frequency(text):
    letters = [x.upper() for x in text if x.upper() in string.ascii_uppercase]
    total = len(letters)
    if total == 0:
        return []
    return [(letter, count, round(100*count/total, 2))
            for letter, count in Counter(letters).most_common()]


def vigenere(text, key, decrypt=True):
    # A=0, B=1, ..., Z=25 (not A=1).
    # With a repeated key: key[position % len(key)].
    if not key or not key.isascii() or not key.isalpha():
        raise ValueError("Key must contain only English letters")
    key = key.upper()
    answer = ""
    used_letters = 0
    for character in text:
        if not character.isascii() or not character.isalpha():
            answer += character
            continue
        shift = ord(key[used_letters % len(key)]) - ord("A")
        if decrypt:
            shift = -shift
        start = ord("A") if character.isupper() else ord("a")
        answer += chr(start + (ord(character) - start + shift) % 26)
        used_letters += 1
    return answer


def index_of_coincidence(text):
    # [EXTRA] High value may mean repeating alphabet patterns / shorter key.
    letters = [c.upper() for c in text if c.upper() in string.ascii_uppercase]
    n = len(letters)
    if n < 2:
        return 0.0
    counts = Counter(letters)
    return sum(v * (v - 1) for v in counts.values()) / (n * (n - 1))


if __name__ == "__main__":
    print("Caesar 'Khoor' possibilities:")
    try_all_caesar("Khoor")
    print("Vigenere example:", vigenere("ihwscsowg", "pass"))
    assert caesar("Hello", 3) == "Khoor"
    assert vigenere(vigenere("HELLO", "KEY", False), "KEY", True) == "HELLO"
