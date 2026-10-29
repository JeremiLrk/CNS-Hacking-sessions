# ORIGINAL CODE — Key standardisation
# This is your submitted solution. Its program logic is unchanged.
# EXAM TIP: read it top to bottom. Python executes top-level statements immediately.
# Look at solution.py for the reusable, beginner-friendly rewrite.
# Input files for this challenge are in the adjacent data/ folder.

# EXPLAINED: Import a Python library so this script can use its functions.
from Crypto.Cipher import DES

# EXPLAINED: Turn printable hexadecimal digits into the real bytes they describe.
ct = bytes.fromhex("74eb40cf03b84d0bc4cd2c6e0fe97fb4e70546d3e09c530d35b344e530351bac")

base = b"IOTDEV"

# EXPLAINED: Repeat the next indented lines for each possible value.
for i in range(256):
    for j in range(256):
        key = base + bytes([i, j])

        # EXPLAINED: Create a DES cipher; this course task restricts the key search.
        cipher = DES.new(key, DES.MODE_ECB)
        pt = cipher.decrypt(ct)

        # EXPLAINED: Run the indented block only when this condition is true.
        if b"cns" in pt or b"CNS" in pt:
            print(f"Key: {key.hex()}, Plaintext: {pt}")