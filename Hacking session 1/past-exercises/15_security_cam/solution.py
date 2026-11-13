"""SECURITY CAM — offline wordlist attack on intercepted RTSP Digest MD5.

WHEN TO TRY: A network capture has 'Digest' auth with:
  username, realm, nonce, method, URI, and the MD5 response.

Compute: HA1 = MD5(username:realm:password)
         HA2 = MD5(method:uri)
         response = MD5(HA1:nonce:HA2)

This is a dictionary attack: read a guessed password from a wordlist,
recalculate the response, compare to the captured one.

The university example uses `rockyou.txt`, which is NOT included here.
Your uploaded `wordlist.txt` is an English dictionary, not necessarily
suitable for password guesses. You can supply a different file.

Run: python 15_security_cam_rtsp_digest.py path/to/rockyou.txt
"""

import hashlib
import sys
from pathlib import Path

USERNAME = "user"
REALM = "PythonRTSP"
METHOD = "DESCRIBE"
URI = "rtsp://cns-test.idlab.uantwerpen.be:50002/video"
NONCE = "4874a055c3f4390506d99e6c51a9e3e360cbef8a62abd7079e11faddcb70a38c"
TARGET_RESPONSE = "b3539154c5b784bba2c47a1a6c7c4ab0"


def md5_hex(data):
    return hashlib.md5(data).hexdigest()


def calculate_digest(password_bytes):
    first_text = f"{USERNAME}:{REALM}:".encode("utf-8") + password_bytes
    ha1 = md5_hex(first_text)

    # HA2 does not depend on password; we'll still show it here for clarity.
    second_text = f"{METHOD}:{URI}".encode("utf-8")
    ha2 = md5_hex(second_text)

    final_text = f"{ha1}:{NONCE}:{ha2}".encode("ascii")
    return md5_hex(final_text)


def try_wordlist(path):
    attempts = 0
    with Path(path).open("rb") as file:
        for raw_line in file:
            # Strip only line endings, not meaningful password spaces.
            password = raw_line.rstrip(b"\r\n")
            attempts += 1

            if calculate_digest(password) == TARGET_RESPONSE:
                print("Password found:", repr(password))
                print("Attempts:", attempts)
                return password

            if attempts % 100000 == 0:
                print("Tried", attempts, "passwords")

    print("No match in this wordlist.")
    return None


def main():
    if len(sys.argv) < 2:
        print("Usage: python 15_security_cam_rtsp_digest.py rockyou.txt")
        print("You must provide a wordlist. rockyou.txt is not bundled.")
        return

    try_wordlist(sys.argv[1])


if __name__ == "__main__":
    main()
