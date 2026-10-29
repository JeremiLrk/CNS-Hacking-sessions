"""[COURSE Part 2] SALSA20 / CHACHA20 examples.

NEED: python -m pip install pycryptodome

WHEN:
- Problem explicitly says Salsa20 or ChaCha20.
- You need to encrypt/decrypt with a KNOWN key + nonce.
- A packet may include `nonce + ciphertext`. Check the challenge description.

Important: you CANNOT decrypt without the key just by having the nonce.
If you know plaintext positions, see `nonce_reuse_solver.py` for XOR tricks.
Never reuse the same secret key+nonce pair for different messages.
"""


def salsa20_encrypt_or_decrypt(data, key, nonce):
    from Crypto.Cipher import Salsa20
    if len(key) not in (16, 32) or len(nonce) != 8:
        raise ValueError("Salsa20: 16/32-byte key and 8-byte nonce")
    cipher = Salsa20.new(key=key, nonce=nonce)
    return cipher.encrypt(data)  # Same operation decrypts when input is ciphertext.


def chacha20_encrypt_or_decrypt(data, key, nonce):
    from Crypto.Cipher import ChaCha20
    cipher = ChaCha20.new(key=key, nonce=nonce)
    return cipher.encrypt(data)  # Raw ChaCha20 is NOT authenticated.


if __name__ == "__main__":
    try:
        secret_key = b"K" * 32
        number_used_once = b"N" * 8
        message = b"Hello CNS"
        encrypted = salsa20_encrypt_or_decrypt(message, secret_key, number_used_once)
        recovered = salsa20_encrypt_or_decrypt(encrypted, secret_key, number_used_once)
        print("Salsa20 result:", recovered)
        assert recovered == message
    except ImportError:
        print("Install pycryptodome to run this example")
