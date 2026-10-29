"""[EXTRA / PREVIOUS] RTSP DIGEST AUTHENTICATION, like the camera exercise.

These are the three formulas for the simple MD5 Digest version (without qop):
    HA1 = MD5(username:realm:password)
    HA2 = MD5(method:uri)
    response = MD5(HA1:nonce:HA2)

WHEN:
- Wireshark shows a RTSP 401 challenge and a WWW-Authenticate nonce.
- You also have the Authorization response from a real request.
- You want to compare passwords from rockyou.txt to the captured response.

Remember: `response` is NOT just MD5(password)! The full formula matters.
"""
import hashlib


def md5(data):
    return hashlib.md5(data).hexdigest()


def response_for_password(password, username, realm, method, uri, nonce):
    # Password comes from binary wordlist, so it is already bytes.
    input1 = f"{username}:{realm}:".encode() + password
    ha1 = md5(input1)
    ha2 = md5(f"{method}:{uri}".encode())
    final_input = f"{ha1}:{nonce}:{ha2}".encode("ascii")
    return md5(final_input)


def crack_from_wordlist(wordlist_path, target_response, username, realm, method, uri, nonce):
    count = 0
    with open(wordlist_path, "rb") as file:
        for line in file:
            password = line.rstrip(b"\r\n")
            count += 1
            candidate = response_for_password(password, username, realm, method, uri, nonce)
            if candidate.lower() == target_response.lower():
                print("MATCH! Password:", repr(password))
                print("Tried:", count)
                return password
            if count % 100000 == 0:
                print("Tried", count, "passwords")
    print("Not found. Check values or wordlist")
    return None


if __name__ == "__main__":
    sample = response_for_password(
        b"test123", "user", "PythonRTSP", "DESCRIBE",
        "rtsp://example.test:50002/video", "abcdef"
    )
    print("Example digest:", sample)
    # To run on your own capture:
    # crack_from_wordlist("rockyou.txt", YOUR_RESPONSE, ...)
