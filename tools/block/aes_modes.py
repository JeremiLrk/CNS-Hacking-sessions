"""[COURSE Part 2] AES: ECB, CBC, CTR and GCM, plus PKCS#7 padding.

NEED: python -m pip install pycryptodome

AES always works internally on 16-byte blocks. Modes decide how MANY blocks
are combined. The mode from your challenge MUST match the mode in your code.

- ECB: no IV. Two identical input blocks can produce identical output blocks.
- CBC: needs 16-byte IV. Usually needs padding.
- CTR: needs unique nonce/counter combination. Behaves like a stream cipher.
- GCM: encrypts AND authenticates. A wrong tag normally causes failure.

WARNING: CTR and Salsa20 nonce reuse can leak data. Reusing for the toy example
is ONLY to demonstrate how encryption and decryption reverse each other.
"""
from collections import Counter


def pad_pkcs7(data, block_size=16):
    # Even when data has exactly 16 bytes, add a FULL block of padding.
    needed = block_size - (len(data) % block_size)
    return data + bytes([needed]) * needed


def unpad_pkcs7(data, block_size=16):
    # Look at the last byte; that number tells how many padding bytes exist.
    if not data or len(data) % block_size:
        raise ValueError("Invalid padded data length")
    number = data[-1]
    if number < 1 or number > block_size or data[-number:] != bytes([number]) * number:
        raise ValueError("Invalid PKCS#7 padding")
    return data[:-number]


def duplicate_aes_blocks(ciphertext):
    # Repeated 16-byte blocks in a ciphertext suggest ECB mode.
    blocks = []
    for index in range(0, len(ciphertext), 16):
        block = ciphertext[index:index+16]
        if len(block) == 16:
            blocks.append(block)
    return [(block.hex(), how_many) for block, how_many in Counter(blocks).items() if how_many > 1]


def aes_ecb(data, key, decrypt=False):
    from Crypto.Cipher import AES
    cipher = AES.new(key, AES.MODE_ECB)
    # Caller handles padding so it is obvious what bytes are being encrypted.
    return cipher.decrypt(data) if decrypt else cipher.encrypt(data)


def aes_cbc(data, key, iv, decrypt=False):
    from Crypto.Cipher import AES
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    return cipher.decrypt(data) if decrypt else cipher.encrypt(data)


def aes_ctr(data, key, nonce, initial_counter=1):
    from Crypto.Cipher import AES
    from Crypto.Util import Counter as CryptoCounter
    if len(nonce) != 8:
        raise ValueError("This demo expects an 8-byte nonce")
    # Very important: initial_counter must be the SAME as in the challenge!
    counter = CryptoCounter.new(64, prefix=nonce, initial_value=initial_counter)
    cipher = AES.new(key, AES.MODE_CTR, counter=counter)
    return cipher.encrypt(data)  # XOR symmetry: same operation decrypts.


def aes_gcm_encrypt(data, key, nonce):
    from Crypto.Cipher import AES
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    encrypted, tag = cipher.encrypt_and_digest(data)
    return encrypted, tag  # SAVE BOTH, or you can't verify later.


def aes_gcm_decrypt(encrypted, key, nonce, tag):
    from Crypto.Cipher import AES
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    return cipher.decrypt_and_verify(encrypted, tag)


def aes_cfb128(data, key, iv, decrypt=False):
    # CFB behaves like a stream. "128" refers to the segment size in BITS.
    # WARNING: some libraries default to 8-bit segments; that gives different output.
    from Crypto.Cipher import AES
    cipher = AES.new(key, AES.MODE_CFB, iv=iv, segment_size=128)
    return cipher.decrypt(data) if decrypt else cipher.encrypt(data)


def aes_ofb(data, key, iv):
    # OFB also behaves like a stream cipher: encryption and decryption are the SAME call.
    from Crypto.Cipher import AES
    cipher = AES.new(key, AES.MODE_OFB, iv=iv)
    return cipher.encrypt(data)


if __name__ == "__main__":
    sample = b"HELLO"
    assert unpad_pkcs7(pad_pkcs7(sample)) == sample
    print("Padding:", pad_pkcs7(sample).hex())
    try:
        key = b"K" * 16
        iv = b"I" * 16
        padded = pad_pkcs7(sample)
        encrypted = aes_cbc(padded, key, iv)
        print("CBC decrypted:", unpad_pkcs7(aes_cbc(encrypted, key, iv, True)))
        nonce = b"N" * 8
        c = aes_ctr(sample, key, nonce)
        assert aes_ctr(c, key, nonce) == sample
        gcm_cipher, tag = aes_gcm_encrypt(sample, key, b"1" * 12)
        assert aes_gcm_decrypt(gcm_cipher, key, b"1" * 12, tag) == sample
    except ImportError:
        print("Install pycryptodome for AES examples")
