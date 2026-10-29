"""[COURSE Part 2 + EXTRA] DES limited-key search.

NEED: python -m pip install pycryptodome

WHEN:
- Your task states DES encryption and gives a special small key format.
- A DES key has 8 bytes. If 6 bytes are KNOWN, only 2 bytes are unknown.

WARNING: the `IOTDEV` prefix was a GUESS for our earlier exercise.
The original prompt does not prove the key is `b'IOTDEV'+two_bytes`.
The script can test this hypothesis; no match does not break DES itself.
"""


def test_keys(ciphertext, known_six_bytes=b"IOTDEV", marker=b"cns", max_results=10):
    from Crypto.Cipher import DES
    if len(known_six_bytes) != 6:
        raise ValueError("Known prefix must have six bytes")
    if len(ciphertext) % 8:
        raise ValueError("DES ECB ciphertext length must be multiple of 8")
    results = []
    for number in range(65536):
        # Example: IOTDEV + 00 00, IOTDEV + 00 01, ..., IOTDEV + ff ff
        key = known_six_bytes + number.to_bytes(2, "big")
        plaintext = DES.new(key, DES.MODE_ECB).decrypt(ciphertext)
        if marker.lower() in plaintext.lower():
            results.append((key, plaintext))
            print("Possible key:", key.hex(), "Result:", repr(plaintext))
            if len(results) >= max_results:
                break
    return results


if __name__ == "__main__":
    ciphertext = bytes.fromhex(
        "74eb40cf03b84d0bc4cd2c6e0fe97fb4e70546d3e09c530d35b344e530351bac"
    )
    try:
        matches = test_keys(ciphertext)
        print("Possible matches:", len(matches))
    except ImportError:
        print("Install pycryptodome first")
