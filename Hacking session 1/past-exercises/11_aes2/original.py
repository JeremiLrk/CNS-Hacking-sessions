# ORIGINAL CODE — AES 2 demo
# This is your submitted solution. Its program logic is unchanged.
# EXAM TIP: read it top to bottom. Python executes top-level statements immediately.
# Look at solution.py for the reusable, beginner-friendly rewrite.
# Input files for this challenge are in the adjacent data/ folder.

with open("enc.bmp", "rb") as f:
    data = f.read()

# EXPLAINED: Repeat the next indented lines for each possible value.
for i in range(0, 64, 16):
    print(f"Offset {i:02d}: {data[i:i+16].hex(' ')}")


start = 54

block = data[start:start + 16]
print("Block:", block.hex())
print("Length:", len(block))

# EXPLAINED: Turn printable hexadecimal digits into the real bytes they describe.
P = bytes.fromhex(
    "0000ff00"
    "00ff0000"
    "ff000000"
    "000000ff"
)

C = data[54:70]
# EXPLAINED: Import a Python library so this script can use its functions.
from Crypto.Cipher import AES

intermediate = {}
for i in range(2**20):
    k1_small = i
    K1 = k1_small.to_bytes(3, "big") + b"\x00" * 13
    # EXPLAINED: Create the AES cipher with the specified key and mode.
    cipher = AES.new(K1, AES.MODE_ECB)
    X = cipher.encrypt(P)
    intermediate[X] = k1_small
print("Stored values:", len(intermediate))


for j in range(2**20):
    k2_small = j
    K2 = k2_small.to_bytes(3, "big") + b"\x00" * 13

    cipher = AES.new(K2, AES.MODE_ECB)
    X = cipher.decrypt(C)

    # EXPLAINED: Run the indented block only when this condition is true.
    if X in intermediate:
        k1_small = intermediate[X]

        K1 = k1_small.to_bytes(3, "big") + b"\x00" * 13
        K2 = k2_small.to_bytes(3, "big") + b"\x00" * 13

        print("K1:", K1.hex())
        print("K2:", K2.hex())
        break



ciphert = bytes.fromhex("df7c7dfbd5e1ba2af108d658132d5f20d34de27da16375ceabd7a79cbfe738244027a4a0b26ec498a2c223a545b9567c20bf423bb38514e6cd6f043ab9e23a84ffa6745294c224068e1cffd9e8c9e294")
cipher2 = AES.new(K2, AES.MODE_ECB)
X = cipher2.decrypt(ciphert)

cipher1 = AES.new(K1, AES.MODE_ECB)
P = cipher1.decrypt(X)

from Crypto.Util.Padding import unpad

P = unpad(P, 16)
print(P.decode())