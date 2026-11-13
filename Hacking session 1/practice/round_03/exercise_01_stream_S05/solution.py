"""S05: same ChaCha20 keystream, DIFFERENT starting counter.

Common mistake: XOR all ciphertexts starting at byte zero.
The secret begins at counter=3, so its first keystream byte is
public keystream byte 3*64 = 192.
"""
from pathlib import Path
HERE = Path(__file__).resolve().parent
CHACHA_BLOCK_BYTES = 64
PUBLIC_COUNTER = 0
SECRET_COUNTER = 3

def xor_bytes(left, right):
    return bytes(a ^ b for a,b in zip(left,right))

def main():
    public_plain = (HERE / "public_plain.bin").read_bytes()
    public_cipher = bytes.fromhex((HERE / "public_cipher.hex").read_text().strip())
    secret_cipher = bytes.fromhex((HERE / "private_cipher.hex").read_text().strip())
    # First recover the bytes of the keystream already seen in public data.
    recovered_stream = xor_bytes(public_plain, public_cipher)
    offset = (SECRET_COUNTER - PUBLIC_COUNTER) * CHACHA_BLOCK_BYTES
    # Match the exact keystream position used by the secret ciphertext.
    stream_for_secret = recovered_stream[offset:offset + len(secret_cipher)]
    if len(stream_for_secret) != len(secret_cipher):
        raise ValueError("Not enough known plaintext to reach the secret counter")
    secret = xor_bytes(secret_cipher, stream_for_secret)
    print("Decrypted:", secret.decode(errors="replace"))
    if b"CODE=" in secret:
        code = secret.split(b"CODE=", 1)[1].strip().split(b";",1)[0]
        print("SUBMIT:", code.decode())

if __name__ == "__main__":
    main()
