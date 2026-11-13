"""S06: recover the seed of a tiny random-number generator.

The seed is only 16 bits: there are 2**16 = 65536 possibilities.
Try ALL seeds; compare the resulting known plaintext prefix.
"""
from pathlib import Path
HERE = Path(__file__).resolve().parent

MULTIPLIER = 20077
INCREMENT = 12345
MODULUS = 65536

def make_keystream(seed, length):
    state = seed
    output = bytearray()
    for _ in range(length):
        # The generator first updates its internal number.
        state = (MULTIPLIER * state + INCREMENT) % MODULUS
        # We use the high eight bits of the new state.
        output.append((state >> 8) & 255)
    return bytes(output)

def xor_bytes(left, right):
    return bytes(a ^ b for a, b in zip(left, right))

def main():
    cipher = bytes.fromhex((HERE / "cipher.hex").read_text().strip())
    known = (HERE / "public_prefix.txt").read_bytes()
    # We test a seed by checking whether decryption starts with the known text.
    for seed in range(2**16):
        stream = make_keystream(seed, len(known))
        first_bytes = xor_bytes(cipher[:len(known)], stream)
        if first_bytes != known:
            continue
        # Found a seed that produces the correct opening text.
        plaintext = xor_bytes(cipher, make_keystream(seed, len(cipher)))
        print("Seed:", seed)
        print("Decrypted:", plaintext.decode(errors="replace"))
        if b"PRIVATE ACCESS=" in plaintext:
            value = plaintext.split(b"PRIVATE ACCESS=", 1)[1].split(b";", 1)[0].strip()
            print("SUBMIT:", value.decode())
        return
    print("No seed matched. Confirm that you copied the generator parameters.")

if __name__ == "__main__":
    main()
