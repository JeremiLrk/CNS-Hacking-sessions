"""B04: change the FIRST plaintext block of CBC by changing its IV.

CBC decryption: P1 = AES_decrypt(C1) XOR IV
Therefore: IV_new = IV_old XOR P_old XOR P_wanted.
This works only when you can change the IV and no MAC/tag rejects it.
"""
from pathlib import Path
HERE = Path(__file__).resolve().parent

def main():
    old_iv = bytes.fromhex((HERE / "iv.hex").read_text().strip())
    old_plaintext = (HERE / "original_block1.txt").read_bytes()
    desired_plaintext = b"access=admin;pad"
    if len(old_iv) != 16 or len(old_plaintext) != 16 or len(desired_plaintext) != 16:
        raise ValueError("Everything must be exactly one AES block = 16 bytes")
    new_iv = bytearray()
    for old_iv_byte, old_plain_byte, new_plain_byte in zip(
        old_iv, old_plaintext, desired_plaintext
    ):
        new_iv.append(old_iv_byte ^ old_plain_byte ^ new_plain_byte)
    print("SUBMIT:", bytes(new_iv).hex())
    print("Keep the ciphertext the same: only the IV was changed.")

if __name__ == "__main__":
    main()
