# ORIGINAL CODE — Secure Bank Salsa20
# This is your submitted solution. Its program logic is unchanged.
# EXAM TIP: read it top to bottom. Python executes top-level statements immediately.
# Look at solution.py for the reusable, beginner-friendly rewrite.
# Input files for this challenge are in the adjacent data/ folder.

# EXPLAINED: Turn printable hexadecimal digits into the real bytes they describe.
ciphertext = bytes.fromhex(
    "ed9c09d1a49ff0ea93fd07694e2940dd6ac4e1fce0927a7d829399849811e7fa80f6fa82f5b4aee33d8ab1875f10f05d0b81899cf9"
)

old = b'000010"}'
new = b'000300"}'

modified = bytearray(ciphertext)

start = len(ciphertext) - len(old)

# EXPLAINED: Repeat the next indented lines for each possible value.
for i in range(len(old)):
    original_byte = old[i]
    desired_byte = new[i]
    xor_difference = original_byte ^ desired_byte
    modified[start + i] = ciphertext[start + i] ^ xor_difference

print(modified.hex())