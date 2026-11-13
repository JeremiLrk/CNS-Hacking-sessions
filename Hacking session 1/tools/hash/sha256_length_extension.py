"""[COURSE Part 3 + EXTRA] SHA-256 LENGTH EXTENSION.

THIS IS ADVANCED. You do not have to understand every bit operation at first.
Think of SHA256 like a machine that processes blocks in order.
Some badly designed authentication uses SHA256(secret + message).
The visible hash exposes the end state of the machine. That lets us
continue hashing MORE message bytes without knowing the secret.

BUT! This does NOT work for real HMAC-SHA256.
It only works for SHA256(secret || message), which is NOT an HMAC.

Use when:
- You know a valid SHA256(secret+message) hash.
- You know the ORIGINAL message.
- You can guess the LENGTH of the secret (not its contents).
- You can append bytes and the server accepts SHA padding bytes.

What you get:
  modified_message = old_message + SHA_padding + your_extra_text
  modified_hash = calculated continuation digest

The code below follows the actual SHA-256 compression rules.
You can call `sha256_length_extension(...)` without changing the internals.
"""
import hashlib
import struct
# SECTION 5 — REAL SHA-256 LENGTH EXTENSION [P3]
# =============================================================================
# If a broken MAC is `SHA256(secret || message)`, and you know the digest and
# guess the LENGTH of secret, you can append data despite not knowing secret.
# HMAC-SHA256 IS NOT VULNERABLE TO THIS ATTACK. SHA3 is not either.
# This code implements SHA256's compression to resume at the old digest state;
# hashlib alone cannot initialize a SHA256 state from a digest.
_SHA256_IV=(0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,
            0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19)
_SHA256_K=(
    0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,
    0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,
    0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,
    0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,
    0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,
    0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,
    0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,
    0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2)
_MASK32=0xffffffff

def _rotr32(x:int,n:int)->int:
    return ((x>>n)|(x<<(32-n)))&_MASK32


def sha256_glue_padding(message_length:int)->bytes:
    """[P3] Padding for Merkle-Damgard SHA256: 0x80 + zeros + 64-bit bit length.
    For forged prefix-MAC, `message_length` must include guessed SECRET length.
    """
    if message_length<0 or message_length>=2**61:raise ValueError('Invalid length')
    return b'\x80'+b'\x00'*((56-(message_length+1)%64)%64)+struct.pack('>Q',message_length*8)


def sha256_compress(state, block):
    """Process ONE 64-byte block, following the official SHA-256 steps.

    Do not edit this math during the exam unless a question specifically
    asks about SHA-256 rounds. The important attacker input is elsewhere:
    the old digest, original message, extra bytes and guessed key LENGTH.
    """
    if len(state) != 8 or len(block) != 64:
        raise ValueError("Need eight state numbers and a 64-byte input block")

    # STEP 1: split the 64-byte block into sixteen 32-bit numbers.
    # > means big-endian. 16I means sixteen unsigned 4-byte integers.
    words = list(struct.unpack(">16I", block))

    # STEP 2: build the remaining 48 numbers (64 total).
    for index in range(16, 64):
        older1 = words[index - 15]
        older2 = words[index - 2]
        small_sigma0 = _rotr32(older1, 7) ^ _rotr32(older1, 18) ^ (older1 >> 3)
        small_sigma1 = _rotr32(older2, 17) ^ _rotr32(older2, 19) ^ (older2 >> 10)
        new_word = words[index - 16] + small_sigma0 + words[index - 7] + small_sigma1
        words.append(new_word & _MASK32)  # Keep ONLY the lowest 32 bits.

    # STEP 3: make working copies of the eight existing SHA256 state numbers.
    a, b, c, d, e, f, g, h = state

    # STEP 4: run 64 rounds, mixing those state numbers.
    for round_number in range(64):
        big_sigma1 = _rotr32(e, 6) ^ _rotr32(e, 11) ^ _rotr32(e, 25)
        choose = (e & f) ^ ((~e) & g)
        first_sum = h + big_sigma1 + choose
        first_sum += _SHA256_K[round_number] + words[round_number]
        first_sum &= _MASK32

        big_sigma0 = _rotr32(a, 2) ^ _rotr32(a, 13) ^ _rotr32(a, 22)
        majority = (a & b) ^ (a & c) ^ (b & c)
        second_sum = (big_sigma0 + majority) & _MASK32

        # Shift the working variables, including new a and new e.
        new_a = (first_sum + second_sum) & _MASK32
        new_e = (d + first_sum) & _MASK32
        h = g
        g = f
        f = e
        e = new_e
        d = c
        c = b
        b = a
        a = new_a

    # STEP 5: add the new state back into the old state, wrapping at 32 bits.
    new_values = (a, b, c, d, e, f, g, h)
    result = []
    for new_value, old_value in zip(new_values, state):
        result.append((new_value + old_value) & _MASK32)
    return tuple(result)


def sha256_continue(digest_hex:str,suffix:bytes,bytes_previously_processed:int)->str:
    """Resume SHA256 at digest state after a full-block padded prefix.
    `bytes_previously_processed` must be divisible by 64 and include OLD glue.
    """
    if bytes_previously_processed%64:raise ValueError('Processed length must align to 64 bytes')
    state=struct.unpack('>8I',bytes.fromhex(digest_hex))
    data=suffix+sha256_glue_padding(bytes_previously_processed+len(suffix))
    for offset in range(0,len(data),64):
        state=sha256_compress(state,data[offset:offset+64])
    return struct.pack('>8I',*state).hex()


def sha256_length_extension(old_digest:str,known_message:bytes,append:bytes,
                            guessed_secret_length:int)->tuple[bytes,str]:
    """[P3] Creates (forged_message, forged_digest) against SHA256(secret||message).

    No claim of success until the target confirms it; try feasible key-length
    guesses if the secret length is not given. The forged message includes
    NON-PRINTABLE SHA256 glue-padding bytes (use HTTP raw body, not casual JSON).
    """
    total=guessed_secret_length+len(known_message)
    glue=sha256_glue_padding(total)
    processed=total+len(glue)
    forged_digest=sha256_continue(old_digest,append,processed)
    return known_message+glue+append,forged_digest


# =============================================================================


if __name__ == "__main__":
    # IMPORTANT: this is a deliberately INSECURE local example.
    # Do not use SHA256(secret + message) as a real MAC.
    secret = b"secret!"
    original = b"action=view"
    extra = b"&admin=1"

    old_digest = hashlib.sha256(secret + original).hexdigest()

    # We do not tell the attack function the secret bytes.
    # We only tell it how many bytes we THINK the secret has.
    changed_message, changed_digest = sha256_length_extension(
        old_digest, original, extra, guessed_secret_length=7
    )

    # Demonstrate that an insecure server would agree.
    server_digest = hashlib.sha256(secret + changed_message).hexdigest()
    print("The SHA-256 length extension works:", changed_digest == server_digest)
    print("Forged message bytes:", repr(changed_message))
    assert changed_digest == server_digest
