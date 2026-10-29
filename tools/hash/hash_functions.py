"""[COURSE Part 3] HASHES, DOUBLE HASHING and HASH VARIANTS.

A hash is like a fingerprint. It is EASY to compute, but you cannot just
reverse it to get the original message back.

WHEN:
- You see a 32-character hex digest (often MD5), 40 (SHA1), 64 (SHA256).
- The exercise asks you to test whether guesses match a target hash.
- You suspect a hash is based on the previous hash.

Warning: length alone does NOT prove which algorithm was used.
"""
import hashlib


def hash_text(text, algorithm="sha256"):
    # Step 1: change text to bytes. Step 2: hash. Step 3: print hex.
    return hashlib.new(algorithm, text.encode("utf-8")).hexdigest()


def hash_bytes(data, algorithm="sha256"):
    # Use this for raw bytes, for instance from bytes.fromhex(...).
    return hashlib.new(algorithm, data).hexdigest()


def compare_double_hash_ways(previous_hex):
    # These are DIFFERENT operations. Test all only when you have a reason.
    old_text = previous_hex.encode("ascii")  # ASCII of the hex digits
    old_raw = bytes.fromhex(previous_hex)     # Actual bytes represented by hex

    # Method A: SHA256 of the old hex TEXT.
    a = hashlib.sha256(old_text).hexdigest()

    # Method B: SHA256 of the old RAW hash bytes.
    b = hashlib.sha256(old_raw).hexdigest()

    # Method C: SHA256(SHA256(old ASCII text)) (double hash).
    first = hashlib.sha256(old_text).digest()
    c = hashlib.sha256(first).hexdigest()

    # Method D: SHA256(SHA256(old raw bytes)) (double raw hash).
    first = hashlib.sha256(old_raw).digest()
    d = hashlib.sha256(first).hexdigest()

    return {"hash_hex_text":a, "hash_raw_bytes":b,
            "double_hex_text":c, "double_raw_bytes":d}


def birthday_collision_example(first_bytes=2, max_attempts=100000):
    # [EXTRA] Demonstrates collisions for a TRUNCATED hash, not full SHA256.
    memory = {}
    for number in range(max_attempts):
        message = str(number).encode()
        short_hash = hashlib.sha256(message).digest()[:first_bytes]
        if short_hash in memory and memory[short_hash] != message:
            return memory[short_hash], message, short_hash.hex()
        memory[short_hash] = message
    return None


if __name__ == "__main__":
    print("MD5('abc'):", hash_text("abc", "md5"))
    print("SHA256('abc'):", hash_text("abc", "sha256"))
    print("Different double hash interpretations:")
    previous = hashlib.sha256(b"hello").hexdigest()
    for name, output in compare_double_hash_ways(previous).items():
        print(name, output)
    print("Truncated collision example:", birthday_collision_example())
    assert hash_text("abc", "md5") == "900150983cd24fb0d6963f7d28e17f72"
