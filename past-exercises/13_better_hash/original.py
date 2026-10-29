# ORIGINAL CODE — Better Hash
# This is your submitted solution. Its program logic is unchanged.
# EXAM TIP: read it top to bottom. Python executes top-level statements immediately.
# Look at solution.py for the reusable, beginner-friendly rewrite.
# Input files for this challenge are in the adjacent data/ folder.

FLAG = "CNS{test-flag}"

# EXPLAINED: Define a reusable function; its body runs when the function is called.
def rol(x, n):
    return ((x << n) | (x >> (8 - n))) & 0xff

def better_hash(msg):
    # EXPLAINED: Convert ordinary text into bytes before performing byte operations.
    state = bytearray(msg.encode())

    # EXPLAINED: Repeat the next indented lines for each possible value.
    for rnd in range(8):

        for i in range(len(state)):
            state[i] ^= (rnd * 41 + i * 17) & 0xff
            state[i] = rol(state[i], (rnd + i) & 7)

        for i in range(1, len(state)):
            state[i] ^= state[i - 1]

        state = state[1:] + state[:1]

    return state.hex()

print(better_hash(FLAG))


def ror(x, n):
    return ((x >> n) | (x << (8 - n))) & 0xff


def reverse_hash(ciphertext):
    state = bytearray.fromhex(ciphertext)
    for rnd in reversed(range(8)):
        state = state[-1:] + state[:-1]

        for i in reversed(range(1, len(state))):
            state[i] ^= state[i - 1]

        for i in reversed(range(len(state))):
            state[i] = ror(state[i], (rnd + i) & 7)
            state[i] ^= (rnd * 41 + i * 17) & 0xff
    return state.decode()




answer = reverse_hash("5f070b54361613bca31a123e95321cff154ba64f549bb34fdc7688f10efb569aed4ccbd6ba")
print(answer)