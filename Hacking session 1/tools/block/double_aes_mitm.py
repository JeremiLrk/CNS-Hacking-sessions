"""[EXTRA] DOUBLE AES with two tiny keys: MEET-IN-THE-MIDDLE (MITM).

NEED: python -m pip install pycryptodome

THE IDEA (like two locks):
1. First lock K1 transforms P into a secret middle value X.
2. Second lock K2 transforms X into ciphertext C.
3. Try all K1 from P, save all middle values.
4. Try all K2 backwards from C, look for matching middle values.

Instead of 2^40 key PAIRS we do about 2 * 2^20 AES steps (plus memory).

!!! VERY IMPORTANT !!!
You need a REAL KNOWN 16-byte plaintext block P and its matching
16-byte ciphertext block C. Guessing BMP pixels is NOT proof.
The real 2^20 search uses lots of memory and takes time.
Run a tiny TEST FIRST to check your code and byte order.
"""


def make_key(number):
    # Exact format from the AES2 challenge:
    # 20-bit number -> THREE bytes -> 13 zero bytes -> AES-128 key.
    return number.to_bytes(3, "big") + b"\x00" * 13


def find_key_pairs(plain_block, cipher_block, bits=8):
    from Crypto.Cipher import AES
    if len(plain_block) != 16 or len(cipher_block) != 16:
        raise ValueError("Need aligned matching 16-byte blocks")
    if bits < 1 or bits > 20:
        raise ValueError("Try 8 for practice, up to 20 for the exercise")
    memory = {}
    number_of_keys = 2 ** bits
    print("Trying", number_of_keys, "possible K1 values")
    for k1 in range(number_of_keys):
        middle = AES.new(make_key(k1), AES.MODE_ECB).encrypt(plain_block)
        memory.setdefault(middle, []).append(k1)
    print("Now trying K2 values backwards")
    matches = []
    for k2 in range(number_of_keys):
        middle = AES.new(make_key(k2), AES.MODE_ECB).decrypt(cipher_block)
        if middle in memory:
            for k1 in memory[middle]:
                matches.append((k1, k2))
                print("Possible key pair:", k1, k2)
    return matches


def decrypt_with_keys(ciphertext, k1, k2):
    from Crypto.Cipher import AES
    # Important: if C = E_K2(E_K1(P)), reverse K2 FIRST, then K1.
    middle = AES.new(make_key(k2), AES.MODE_ECB).decrypt(ciphertext)
    return AES.new(make_key(k1), AES.MODE_ECB).decrypt(middle)


if __name__ == "__main__":
    try:
        from Crypto.Cipher import AES
        known_plaintext = b"ABCDEFGHIJKLMNOP"
        real_k1, real_k2 = 3, 7
        x = AES.new(make_key(real_k1), AES.MODE_ECB).encrypt(known_plaintext)
        encrypted = AES.new(make_key(real_k2), AES.MODE_ECB).encrypt(x)
        matches = find_key_pairs(known_plaintext, encrypted, bits=4)
        print("Real pair found?", (real_k1, real_k2) in matches)
        assert (real_k1, real_k2) in matches
        assert decrypt_with_keys(encrypted, real_k1, real_k2) == known_plaintext
    except ImportError:
        print("Install pycryptodome for this example")
