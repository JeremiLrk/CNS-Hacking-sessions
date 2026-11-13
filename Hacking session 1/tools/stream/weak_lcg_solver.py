"""[EXTRA] WEAK CUSTOM RANDOM GENERATOR (LCG) — example from CNS.

WHEN TO USE:
- The challenge GIVES you source code for a random number generator.
- It uses a very simple formula like (A * state + C) % M.
- The ciphertext uses XOR with output bytes from that random generator.

This file matches the PARTICULAR custom cipher used in our earlier exercise.
It is NOT a general Salsa20 or SHA256 cracker!
"""

A = 1103515245
C = 12345
MODULUS = 2**31


def next_state(previous_state):
    # One new internal number from the previous internal number.
    return (A * previous_state + C) % MODULUS


def create_keystream(seed, number_of_bytes):
    # Use the same formula the challenge source uses.
    state = seed
    answer = bytearray()
    for _ in range(number_of_bytes):
        state = next_state(state)
        one_byte = (state >> 16) & 255
        answer.append(one_byte)
    return bytes(answer)


def xor(left, right):
    if len(left) != len(right):
        raise ValueError("Lengths must match")
    return bytes(a ^ b for a, b in zip(left, right))


def find_possible_seeds(known_keystream, stop_after=5):
    # We know output_byte = (state >> 16) & 255.
    # That reveals ONLY 8 bits of state, not all 31 bits.
    # First state still has 7 unknown HIGH bits and 16 LOW bits.
    # We test all 2^(7+16) possibilities and compare later bytes.
    if len(known_keystream) < 3:
        raise ValueError("Use at least three known keystream bytes")
    wanted_first_byte = known_keystream[0]
    reverse_multiplier = pow(A, -1, MODULUS)
    found = []
    for high_bits in range(128):
        partly_known_state = (high_bits << 24) | (wanted_first_byte << 16)
        for low_bits in range(65536):
            first_state = partly_known_state | low_bits
            state = first_state
            looks_correct = True
            for expected_byte in known_keystream[1:]:
                state = next_state(state)
                if ((state >> 16) & 255) != expected_byte:
                    looks_correct = False
                    break
            if looks_correct:
                # Reverse the FIRST state update to retrieve a possible seed.
                seed = ((first_state - C) * reverse_multiplier) % MODULUS
                found.append(seed)
                if len(found) >= stop_after:
                    return found
    return found


if __name__ == "__main__":
    seed = 12345
    stream = create_keystream(seed, 10)
    original = b"hello!!!!!"
    ciphertext = xor(original, stream)
    print("Ciphertext:", ciphertext.hex())
    print("Recovered text if seed known:", xor(ciphertext, create_keystream(seed, 10)))
    assert xor(ciphertext, stream) == original
    # `find_possible_seeds` takes longer; use with KNOWN keystream in real exercise.
