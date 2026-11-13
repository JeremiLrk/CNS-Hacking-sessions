"""H02: dictionary attack on a badly-described DOUBLE SHA-256.

Be careful: digest() returns raw bytes; hexdigest() returns ASCII text.
The developer explicitly used SHA256(SHA256(password).hexdigest().encode()).
This is different from SHA256(SHA256(password).digest()).
"""
import hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent

def hash_like_developer(password):
    first_hash_as_hex_text = hashlib.sha256(password).hexdigest()
    # Example: first_hash_as_hex_text contains 64 printable characters.
    return hashlib.sha256(first_hash_as_hex_text.encode('ascii')).hexdigest()

def main():
    expected = (HERE/'stored_hash.txt').read_text().strip().lower()
    for line in (HERE/'candidate_passwords.txt').read_bytes().splitlines():
        # Work in raw bytes so strange password characters don't get corrupted.
        password = line.rstrip(b'\r\n')
        if hash_like_developer(password) == expected:
            print('SUBMIT:',password.decode('utf-8',errors='replace'))
            return
    print('Password not found. Check exact hash order and data type.')

if __name__=='__main__':
    main()
