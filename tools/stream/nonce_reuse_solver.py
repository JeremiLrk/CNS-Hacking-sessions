"""[COURSE Part 2] + [EXTRA] STREAM / AES-CTR / SALSA20 NONCE REUSE.

WHAT TO TRY:
1. Did two encrypted messages use the SAME key, SAME nonce, SAME counter start?
2. Do you know the plaintext of ONE message?
3. If yes, compute the keystream and XOR with the other ciphertext.

NOTE: "nonce" means a number that must not repeat with the same key.
If two messages use DIFFERENT nonces, this exact attack normally DOES NOT work.
"""

def xor_prefix(left, right):
    # We use min length because maybe we only know a prefix of a message.
    # Only this matching prefix can be recovered with certainty.
    return bytes(a ^ b for a, b in zip(left, right))


def recover_keystream(known_text, known_cipher):
    # C1 = P1 XOR S  ->  S = P1 XOR C1
    return xor_prefix(known_text, known_cipher)


def decrypt_second_message(known_text, known_cipher, secret_cipher):
    # First get S from the message you know.
    stream = recover_keystream(known_text, known_cipher)
    # Then P2 = C2 XOR S.
    return xor_prefix(secret_cipher, stream)


def change_ciphertext(ciphertext, position, old_plaintext, new_plaintext):
    # This is called "bit flipping" or stream malleability.
    # It does NOT reveal the key.
    # Only use it if you know the old bytes at this exact position!
    # NEW LENGTH MUST BE THE SAME AS OLD LENGTH.
    if len(old_plaintext) != len(new_plaintext):
        raise ValueError("Old and new text must have the same length")
    if position < 0 or position + len(old_plaintext) > len(ciphertext):
        raise ValueError("You selected a position outside the ciphertext")
    answer = bytearray(ciphertext)
    for index in range(len(old_plaintext)):
        difference = old_plaintext[index] ^ new_plaintext[index]
        answer[position + index] ^= difference
    return bytes(answer)


def split_salsa_packet(packet, nonce_size=8):
    # SecureBank hint: packet = 8-byte nonce + ciphertext.
    # Never apply XOR to the nonce while editing message bytes.
    return packet[:nonce_size], packet[nonce_size:]


if __name__ == "__main__":
    known = b"HELLO!"
    secret = b"SECRET"
    stream = b"abcdef"  # Example: a reused keystream. NOT secure use.
    cipher1 = xor_prefix(known, stream)
    cipher2 = xor_prefix(secret, stream)
    print("Recovered second message:", decrypt_second_message(known, cipher1, cipher2))
    assert decrypt_second_message(known, cipher1, cipher2) == secret
    # Change known plaintext without knowing the secret keystream.
    updated = change_ciphertext(cipher1, 0, b"HELLO!", b"BYE!!!")
    assert xor_prefix(updated, stream) == b"BYE!!!"
