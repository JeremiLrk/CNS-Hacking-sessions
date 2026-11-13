"""SPACE RACE 1 — your SHA-256 step, made readable.

STATUS: SOLVED BY YOU (user-confirmed).
THIS FILE'S TEST STATUS: The assistant did not reconnect to the lab server.

This file explains exactly what YOUR uploaded Space Race.py does:
 - Read a string that looks like hexadecimal data.
 - Turn that hex text into REAL bytes.
 - Hash those raw bytes using SHA-256.
 - Print the new digest as hexadecimal text.

Example:
    "4142" (four hex characters) --> b"AB" (two bytes)
    SHA256(b"AB") differs from SHA256(b"4142").

The uploaded snippet is one step from your solved exercise. It does not
include the server conversation, so we don't invent extra steps or claim
we independently reproduced a live flag.
"""

import hashlib


def sha256_of_hex_bytes(hex_text):
    """Decode hex first, THEN compute SHA-256 of the resulting bytes."""
    # Strip accidental spaces/newlines when pasting an input.
    clean_hex = hex_text.strip()

    # Each TWO hex digits stand for one byte.
    raw_bytes = bytes.fromhex(clean_hex)

    # .digest() gives raw bytes; .hexdigest() gives a printable hex string.
    next_hash = hashlib.sha256(raw_bytes).hexdigest()
    return next_hash


def main():
    previous = input("Paste the hex value from the challenge: ")
    next_hash = sha256_of_hex_bytes(previous)
    print("SHA-256 after decoding hex:", next_hash)


if __name__ == "__main__":
    main()
