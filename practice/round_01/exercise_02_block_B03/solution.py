"""B03: cut-and-paste ECB blocks.

AES-ECB encrypts each 16-byte block separately. A block of ciphertext
can be moved to another position, if the receiving format accepts it.
No secret AES key is needed; this is NOT decrypting AES.
"""
from pathlib import Path
HERE = Path(__file__).resolve().parent
BLOCK_SIZE = 16

def main():
    original = bytes.fromhex((HERE / "original_request.hex").read_text().strip())
    admin_block = bytes.fromhex((HERE / "admin_role_block.hex").read_text().strip())
    if len(original) != 3 * BLOCK_SIZE:
        raise ValueError("Original request should contain exactly 3 blocks")
    if len(admin_block) != BLOCK_SIZE:
        raise ValueError("ADMIN ciphertext must contain exactly one block")
    first_block = original[0:16]  # Keep CMD=OPEN block
    third_block = original[32:48] # Keep ZONE=SAFE block
    forged = first_block + admin_block + third_block
    print("SUBMIT:", forged.hex())
    print("Number of ciphertext bytes:",len(forged))

if __name__ == "__main__":
    main()
