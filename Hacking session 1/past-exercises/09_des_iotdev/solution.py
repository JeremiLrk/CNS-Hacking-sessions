"""KEY STANDARDISATION — DES key search with a guessed known prefix.

WHEN TO TRY: The challenge hints that part of a short DES key is standard.
Example hypothesis: key = b'IOTDEV' + two unknown bytes (65536 candidates).

The course sample ciphertext HAS now been independently decrypted with
this guess: the decoded plaintext contains cns{i-have-room-temperature-iq}.
DES parity bits cause several 8-byte keys to behave identically.

Requires: python -m pip install pycryptodome
"""

CIPHERTEXT_HEX = "74eb40cf03b84d0bc4cd2c6e0fe97fb4e70546d3e09c530d35b344e530351bac"
KEY_PREFIX = b"IOTDEV"


def find_possible_keys(ciphertext, prefix=KEY_PREFIX):
    from Crypto.Cipher import DES
    if len(prefix) != 6:
        raise ValueError("This search assumes a six-byte prefix")
    if len(ciphertext) % 8 != 0:
        raise ValueError("DES-ECB needs blocks of 8 ciphertext bytes")

    for first in range(256):
        for second in range(256):
            key = prefix + bytes([first, second])
            plaintext = DES.new(key, DES.MODE_ECB).decrypt(ciphertext)

            # A recognizable flag is evidence; check any hit carefully.
            if b"cns{" in plaintext.lower():
                yield key, plaintext


def main():
    ciphertext = bytes.fromhex(CIPHERTEXT_HEX)
    found = False
    for key, plaintext in find_possible_keys(ciphertext):
        found = True
        print("Candidate key:", key.hex())
        print("Plaintext:", plaintext)
    if not found:
        print("No match; check the DES mode and prefix.")


if __name__ == "__main__":
    main()
