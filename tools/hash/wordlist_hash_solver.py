"""[COURSE Part 3 + EXTRA] FIND A PASSWORD USING A WORDLIST.

Imagine a list of possible passwords: apple, cat, password123...
We try one at a time, hash it, and compare with the target.
This is a DICTIONARY ATTACK, not a magic reverse-hash algorithm.

WHEN TO USE:
- You have a leaked password hash and a known hash algorithm.
- You have `rockyou.txt` or another list of candidate passwords.
- You know whether the server used a salt and which order.

IMPORTANT: Use `rb` so weird bytes in the wordlist won't crash UTF-8 decoding.
"""
import hashlib
from pathlib import Path


def calculate_hash(password, method="sha256", salt=b"", salt_mode="none"):
    # The challenge may do SHA256(password), SHA256(salt+password), etc.
    if salt_mode == "none":
        message = password
    elif salt_mode == "salt_first":
        message = salt + password
    elif salt_mode == "salt_last":
        message = password + salt
    else:
        raise ValueError("Unknown salt_mode")
    return hashlib.new(method, message).hexdigest()


def search_password(wordlist, target_hash, method="sha256", salt=b"", salt_mode="none"):
    number_tested = 0
    with open(wordlist, "rb") as file:
        for line in file:
            # Remove ONLY newline; a space might be part of the password.
            password = line.rstrip(b"\r\n")
            number_tested += 1
            result = calculate_hash(password, method, salt, salt_mode)
            if result.lower() == target_hash.lower():
                print("PASSWORD FOUND:", repr(password))
                print("Attempts:", number_tested)
                return password
            if number_tested % 100000 == 0:
                print("Checked", number_tested, "candidates")
    print("No match in this wordlist; check algorithm, salt and encoding")
    return None


def pbkdf2_demo(password, salt, iterations=100000):
    # PBKDF2 is designed to make guessing passwords more expensive.
    return hashlib.pbkdf2_hmac("sha256", password, salt, iterations)


def scrypt_demo(password, salt):
    # Scrypt makes each guess require significant memory too.
    return hashlib.scrypt(password, salt=salt, n=2**14, r=8, p=1)


if __name__ == "__main__":
    from tempfile import TemporaryDirectory
    target = hashlib.md5(b"hello123").hexdigest()
    with TemporaryDirectory() as temp:
        file = Path(temp) / "little_wordlist.txt"
        file.write_bytes(b"cat\npassword\nhello123\n")
        assert search_password(file, target, method="md5") == b"hello123"
    print("For your own file: search_password('rockyou.txt', TARGET, 'md5')")
