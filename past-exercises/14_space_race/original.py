# ORIGINAL CODE — Space Race 1
# This is your submitted solution. Its program logic is unchanged.
# EXAM TIP: read it top to bottom. Python executes top-level statements immediately.
# Look at solution.py for the reusable, beginner-friendly rewrite.
# Input files for this challenge are in the adjacent data/ folder.

# EXPLAINED: Import a Python library so this script can use its functions.
import hashlib
previous = input()
# EXPLAINED: Turn printable hexadecimal digits into the real bytes they describe.
data = bytes.fromhex(previous)
# EXPLAINED: Calculate a cryptographic digest of the bytes supplied here.
second = hashlib.sha256(data).hexdigest()

print(second)