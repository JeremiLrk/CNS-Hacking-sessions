"""[COURSE Part 2] XOR — probably THE MOST IMPORTANT operation in stream ciphers.

Think of XOR as a tiny switch:
    same bits -> 0
    different bits -> 1

The key trick is: A XOR B XOR B = A.
So if C = P XOR KEYSTREAM, then P = C XOR KEYSTREAM.
"""

def xor_bytes(first, second):
    # zip puts bytes in pairs, e.g. (first[0],second[0]).
    # ^ means XOR in Python.
    if len(first) != len(second):
        raise ValueError("Both inputs must have the same number of bytes")
    result = bytearray()
    for left, right in zip(first, second):
        result.append(left ^ right)
    return bytes(result)


def xor_repeated_key(message, key):
    # Repeat a short key until it covers the whole message.
    # This is a TOY encryption technique, not secure modern crypto.
    if not key:
        raise ValueError("Key cannot be empty")
    result = bytearray()
    for position, letter in enumerate(message):
        key_byte = key[position % len(key)]
        result.append(letter ^ key_byte)
    return bytes(result)


def single_byte_xor_crack(ciphertext):
    # [EXTRA] When a message was XORed with ONE byte, only 256 keys exist.
    # Try every key and print the candidates that look most like English.
    common_letters = b" etaoinshrdluETAOINSHRDLU"
    possibilities = []
    for key in range(256):
        candidate = bytes(character ^ key for character in ciphertext)
        score = sum(character in common_letters for character in candidate)
        # Punish bytes that look very unlikely in normal text.
        score -= sum(character < 9 or 13 < character < 32 for character in candidate) * 3
        possibilities.append((score, key, candidate))
    return sorted(possibilities, reverse=True)


if __name__ == "__main__":
    message = b"hello"
    key = b"KEY"
    encrypted = xor_repeated_key(message, key)
    decrypted = xor_repeated_key(encrypted, key)
    print("Encrypted (hex):", encrypted.hex())
    print("Decrypted:", decrypted)
    assert decrypted == message
    assert xor_bytes(b"abc", b"abc") == b"\x00\x00\x00"
