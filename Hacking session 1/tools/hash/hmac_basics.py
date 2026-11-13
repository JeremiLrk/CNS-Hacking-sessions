"""[COURSE Part 3] HMAC: a hash that also needs a SECRET KEY.

Think of an HMAC like a fingerprint with a private password hidden inside.
The sender and receiver both know the secret. An attacker shouldn't.

HMAC-SHA256 is NOT the same as SHA256(secret + message).
Correct HMAC is protected against ordinary SHA256 length extension.
"""
import hashlib
import hmac


def make_hmac(secret_key, message, algorithm="sha256"):
    # Both inputs MUST be bytes.
    return hmac.new(secret_key, message, algorithm).hexdigest()


def check_hmac(secret_key, message, received_hex, algorithm="sha256"):
    correct_hex = make_hmac(secret_key, message, algorithm)
    # Better than comparing secret values character-by-character with ==.
    return hmac.compare_digest(correct_hex, received_hex.lower())


if __name__ == "__main__":
    key = b"secret"
    message = b'{"role":"guest"}'
    signature = make_hmac(key, message)
    print("Signature:", signature)
    print("Original matches?", check_hmac(key, message, signature))
    print("Changed message matches?", check_hmac(key, b'{"role":"admin"}', signature))
    assert check_hmac(key, message, signature)
    assert not check_hmac(key, b'{"role":"admin"}', signature)
