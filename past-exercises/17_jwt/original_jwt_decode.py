# ORIGINAL CODE — Token of Trust
# This is your submitted solution. Its program logic is unchanged.
# EXAM TIP: read it top to bottom. Python executes top-level statements immediately.
# Look at solution.py for the reusable, beginner-friendly rewrite.
# Input files for this challenge are in the adjacent data/ folder.

# EXPLAINED: Import a Python library so this script can use its functions.
import base64
import json

payload = "eyJzdWIiOiJhbGljZSIsInJvbGUiOiJndWVzdCJ9"

decoded = base64.urlsafe_b64decode(payload + "==")
data = json.loads(decoded)

print(data)