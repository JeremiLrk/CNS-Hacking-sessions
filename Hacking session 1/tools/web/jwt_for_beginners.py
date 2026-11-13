"""[EXTRA / PREVIOUS] JWT: HEADER.PAYLOAD.SIGNATURE.

A JWT is three pieces with dots between them.
The FIRST TWO are base64url-encoded JSON and can be READ without a secret.
The THIRD is a cryptographic signature/MAC. You normally need the secret
or private key to create a NEW VALID signed token.

IMPORTANT:
- Decoding is NOT the same as verifying the signature.
- JWT 'alg: none' was accepted by one deliberately vulnerable CNS lab.
- Real secure servers should reject that where signatures are required.
"""
import base64
import hashlib
import hmac
import json


def encode_part(data):
    # JSON -> bytes -> URL-safe Base64 -> remove equals signs.
    raw = json.dumps(data, separators=(",", ":")).encode("utf-8")
    return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")


def decode_part(encoded_part):
    # Add missing Base64 equals padding, decode bytes, parse JSON.
    encoded_part += "=" * (-len(encoded_part) % 4)
    raw = base64.urlsafe_b64decode(encoded_part)
    return json.loads(raw)


def read_jwt_without_verifying(token):
    pieces = token.split(".")
    if len(pieces) != 3:
        raise ValueError("JWT should contain exactly two dots")
    return decode_part(pieces[0]), decode_part(pieces[1]), pieces[2]


def create_hs256_token(header, payload, secret):
    # For your own *toy/local* token; NOT for forging unknown-key tokens.
    header64 = encode_part(header)
    payload64 = encode_part(payload)
    signed_text = (header64 + "." + payload64).encode("ascii")
    signature = hmac.new(secret, signed_text, hashlib.sha256).digest()
    signature64 = base64.urlsafe_b64encode(signature).decode().rstrip("=")
    return header64 + "." + payload64 + "." + signature64


def verify_hs256(token, secret):
    # Safe basic example for locally signed tokens with an EXPLICIT allowed alg.
    header, payload, signature64 = read_jwt_without_verifying(token)
    if header.get("alg") != "HS256":
        return False
    before_signature = token.rsplit(".", 1)[0].encode("ascii")
    expected = hmac.new(secret, before_signature, hashlib.sha256).digest()
    received = base64.urlsafe_b64decode(signature64 + "=" * (-len(signature64) % 4))
    return hmac.compare_digest(expected, received)


def insecure_none_lab_demo(header, payload):
    # LAB DEMO ONLY: illustrates an *unsigned* token; secure servers reject it.
    header = dict(header)
    header["alg"] = "none"
    return encode_part(header) + "." + encode_part(payload) + "."


if __name__ == "__main__":
    secret = b"local-only-secret"
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {"user": "guest", "role": "user"}
    token = create_hs256_token(header, payload, secret)
    print("JWT:", token)
    print("Decoded:", read_jwt_without_verifying(token))
    assert verify_hs256(token, secret)
    print("Unsigned example:", insecure_none_lab_demo(header, {"role":"admin"}))
