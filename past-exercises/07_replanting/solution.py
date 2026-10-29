"""REPLANTING — known plaintext + weak linear congruential generator.

WHEN TO TRY: You receive PRNG code, a known plaintext/ciphertext pair,
and another ciphertext generated using the same hidden seed.

1. First recover the first keystream bytes: K = P XOR C.
2. For the FIRST keystream byte, only bits 16..23 of the PRNG state are known.
3. Try missing state bits, checking every new keystream byte.
4. Reverse one PRNG step to obtain a possible seed.
5. Verify the seed regenerates the ENTIRE known ciphertext before using it.

Several seeds may be indistinguishable: never claim unique recovery without proof.
"""

from pathlib import Path

A = 1103515245
B = 12345
MODULUS = 2 ** 31
DATA = Path(__file__).resolve().parent / "data"


def next_state(state):
    return (A * state + B) % MODULUS


def keystream(seed, length):
    state = seed
    output = bytearray()
    for _ in range(length):
        state = next_state(state)
        output.append((state >> 16) & 255)
    return bytes(output)


def xor_bytes(first, second):
    return bytes(a ^ b for a, b in zip(first, second))


def possible_seeds(known_stream):
    # The first output byte reveals 8 bits of the FIRST next_state.
    # Our state has 31 bits; that leaves 23 unknown bits.
    first_byte = known_stream[0]
    inverse_a = pow(A, -1, MODULUS)

    for upper_bits in range(128):
        for lower_bits in range(65536):
            first_state = (upper_bits << 24) | (first_byte << 16) | lower_bits
            state = first_state
            matching = True

            for expected_byte in known_stream[1:]:
                state = next_state(state)
                produced_byte = (state >> 16) & 255
                if produced_byte != expected_byte:
                    matching = False
                    break

            if matching:
                original_seed = ((first_state - B) * inverse_a) % MODULUS
                yield original_seed


def main():
    public_text = (DATA / "public.txt").read_text(encoding="utf-8")
    # File contains labels, a plaintext line, and a hex string.
    known_plaintext = public_text.split("Known plaintext:")[1].split("Ciphertext:")[0].strip().encode()
    known_hex = public_text.split("Ciphertext:")[1].strip()
    known_ciphertext = bytes.fromhex(known_hex)
    target_ciphertext = bytes.fromhex((DATA / "secret.txt").read_text().strip())

    known_stream = xor_bytes(known_plaintext, known_ciphertext)
    for seed in possible_seeds(known_stream):
        if xor_bytes(known_plaintext, keystream(seed, len(known_plaintext))) != known_ciphertext:
            continue
        candidate_plaintext = xor_bytes(target_ciphertext, keystream(seed, len(target_ciphertext)))
        print("Matching seed candidate:", seed)
        print("Decrypted message:", candidate_plaintext.decode(errors="replace"))
        # Could be more candidates, but one with valid plaintext often suffices.
        return
    print("No matching seed found. Check both files and the PRNG constants.")


if __name__ == "__main__":
    main()
