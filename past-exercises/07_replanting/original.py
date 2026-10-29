# ORIGINAL CODE — Replanting
# This is your submitted solution. Its program logic is unchanged.
# EXAM TIP: read it top to bottom. Python executes top-level statements immediately.
# Look at solution.py for the reusable, beginner-friendly rewrite.
# Input files for this challenge are in the adjacent data/ folder.

"""
Encryption module.

This module implements a custom stream cipher.
"""

# LCG parameters
A = 1103515245
C = 12345
M = 2**31


# EXPLAINED: Define a reusable function; its body runs when the function is called.
def next_state(state):
    """Generate the next PRNG state."""
    return (A * state + C) % M


def generate_keystream(seed, length):
    """Generate a pseudorandom keystream."""
    state = seed
    keystream = bytearray()

    # EXPLAINED: Repeat the next indented lines for each possible value.
    for _ in range(length):
        state = next_state(state)
        keystream.append((state >> 16) & 0xff)

    return bytes(keystream)


def encrypt(plaintext, seed):
    """Encrypt plaintext using XOR."""
    keystream = generate_keystream(seed, len(plaintext))
    return bytes(
        # EXPLAINED: Pair items from two inputs. zip() stops at the shorter input.
        p ^ k for p, k in zip(plaintext, keystream)
    )


def decrypt(ciphertext, seed):
    """Decrypt ciphertext using XOR."""
    return encrypt(ciphertext, seed)


def find_keystream(ciphertext, plaintext):
    # EXPLAINED: Turn printable hexadecimal digits into the real bytes they describe.
    ciphertext_bytes = bytes.fromhex(ciphertext)
    # EXPLAINED: Convert ordinary text into bytes before performing byte operations.
    plaintext_bytes = plaintext.encode()
    keystream = bytearray()
    # ciphertext = plaintext XOR keystream
    # therefore keystream = plaintext XOR ciphertext
    for p, c in zip(plaintext_bytes, ciphertext_bytes):
        keystream.append(p ^ c)
    return bytes(keystream)

def find_seed(keystream):
    first_byte = keystream[0]

    for upper_bits in range(2**7):
        for lower_bits in range(2**16):
            state = (upper_bits << 24) | (first_byte << 16) | lower_bits
            test_state = state
            for i in range(1, len(keystream)):
                test_state = next_state(test_state)
                # EXPLAINED: Run the indented block only when this condition is true.
                if ((test_state >> 16) & 0xff) != keystream[i]:
                    break
            else:
                seed = (state - C) * pow(A, -1, M) % M
                return seed


key_stream = find_keystream("22135cc0b9daa9e717f98a998e6ee5e92655e1a88f", "STATUS: SERVER ONLINE")
seed = find_seed(key_stream)
answer = decrypt(bytes.fromhex("12296eef9eece6b42dd2bf90aa63b6d21a7cc98b95c78b4b01d833d628a941b82fb65176b4ed3c3f64"), seed)
print(answer.decode())