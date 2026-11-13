"""SECURE BANK — modify known Salsa20 ciphertext bytes without learning the key.

WHEN TO TRY: A stream cipher protects data, but there is NO MAC or tag.
For a stream cipher, ciphertext = plaintext XOR keystream.
If you know the original plaintext at the exact position you want to change:

new_cipher_byte = old_cipher_byte XOR old_plain_byte XOR desired_plain_byte

It is safest to replace a string with one of the SAME byte length.
IMPORTANT: the server's wire format may be NONCE (first 8 bytes) + CIPHERTEXT.
Never mutate the nonce. Confirm the JSON serialization and offsets first.
"""

SAMPLE_CIPHERTEXT_HEX = (
    "ed9c09d1a49ff0ea93fd07694e2940dd6ac4e1fce0927a7d829399849811e7fa"
    "80f6fa82f5b4aee33d8ab1875f10f05d0b81899cf9"
)
OLD_TEXT = b'000010"}'
NEW_TEXT = b'000300"}'


def modify_known_plaintext(ciphertext, old_text, new_text, start):
    if len(old_text) != len(new_text):
        raise ValueError("Old and new text must have identical byte lengths")
    if start < 0 or start + len(old_text) > len(ciphertext):
        raise ValueError("Offset is outside ciphertext")

    modified = bytearray(ciphertext)
    for index in range(len(old_text)):
        difference = old_text[index] ^ new_text[index]
        modified[start + index] ^= difference

    return bytes(modified)


def main():
    ciphertext = bytes.fromhex(SAMPLE_CIPHERTEXT_HEX)
    # This original example assumes the known value is at the END.
    offset = len(ciphertext) - len(OLD_TEXT)
    changed = modify_known_plaintext(ciphertext, OLD_TEXT, NEW_TEXT, offset)
    print("Modified ciphertext:", changed.hex())
    print("If received data includes nonce+ciphertext, split them first.")


if __name__ == "__main__":
    main()
