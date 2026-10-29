# ORIGINAL CODE — The French Cipher
# This is your submitted solution. Its program logic is unchanged.
# EXAM TIP: read it top to bottom. Python executes top-level statements immediately.
# Look at solution.py for the reusable, beginner-friendly rewrite.
# Input files for this challenge are in the adjacent data/ folder.

# Vigenere cipher

alphabet = {
    "a": 1,
    "b": 2,
    "c": 3,
    "d": 4,
    "e": 5,
    "f": 6,
    "g": 7,
    "h": 8,
    "i": 9,
    "j": 10,
    "k": 11,
    "l": 12,
    "m": 13,
    "n": 14,
    "o": 15,
    "p": 16,
    "q": 17,
    "r": 18,
    "s": 19,
    "t": 20,
    "u": 21,
    "v": 22,
    "w": 23,
    "x": 24,
    "y": 25,
    "z": 26
}

x = input("Enter the cyphertext: ")
y = input("Enter the key: ")

keylen = len(y)

result = []

# EXPLAINED: Repeat the next indented lines for each possible value.
for index, letter in enumerate(x):

    # EXPLAINED: Run the indented block only when this condition is true.
    if letter == '-' or letter == '{' or letter == '}':
        result.append(letter)
        continue

    cipher_val = alphabet[letter]

    key_letter = y[index % keylen]
    key_val = alphabet[key_letter]

    plain = ((cipher_val - 1) - (key_val - 1)) % 26 + 1

    for key, value in alphabet.items():
        if value == plain:
            result.append(key)
            break

print("The plaintext is:", ''.join(result))