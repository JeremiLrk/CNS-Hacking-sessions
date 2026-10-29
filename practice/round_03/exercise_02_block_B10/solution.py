"""B10: double AES with SMALL keys: meet in the middle.

Naive attack: try every (k1,k2) pair => 4096 * 4096 = 16 million trials.
Meet-in-the-middle:
  - store AES(K1, plaintext) for every possible K1
  - search AES_DECRYPT(K2, ciphertext) for every K2
  - keep pairs where intermediate blocks match
  - test pair 2 so a wrong collision does not fool you

Needs: pip install cryptography
"""
import json
from pathlib import Path
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
HERE=Path(__file__).resolve().parent

def aes_key(small_number):
    # Exactly as the challenge says: two-byte big-endian number, 14 zero bytes.
    return small_number.to_bytes(2,"big") + b"\x00"*14

def encrypt_block(key,block):
    encryptor=Cipher(algorithms.AES(key),modes.ECB()).encryptor()
    return encryptor.update(block)+encryptor.finalize()

def decrypt_block(key,block):
    decryptor=Cipher(algorithms.AES(key),modes.ECB()).decryptor()
    return decryptor.update(block)+decryptor.finalize()

def main():
    data=json.loads((HERE/"pairs.json").read_text())
    first,second=data["known_pairs"]
    p1=bytes.fromhex(first["plaintext_hex"])
    c1=bytes.fromhex(first["ciphertext_hex"])
    p2=bytes.fromhex(second["plaintext_hex"])
    c2=bytes.fromhex(second["ciphertext_hex"])
    limit=2**data["small_bits"]
    forward={}
    for small_k1 in range(limit):
        middle=encrypt_block(aes_key(small_k1),p1)
        # Store possible keys for each intermediate block.
        forward.setdefault(middle,[]).append(small_k1)
    for small_k2 in range(limit):
        middle=decrypt_block(aes_key(small_k2),c1)
        if middle not in forward:
            continue
        for small_k1 in forward[middle]:
            # Verify the SECOND message with the candidate keys.
            middle2=encrypt_block(aes_key(small_k1),p2)
            if encrypt_block(aes_key(small_k2),middle2)==c2:
                print("SUBMIT:", f"{small_k1},{small_k2}")
                return
    print("No matching keys found")

if __name__=="__main__":
    main()
