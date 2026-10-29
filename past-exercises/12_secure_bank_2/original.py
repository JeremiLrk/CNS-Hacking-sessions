# ORIGINAL CODE — Secure Bank 2
# This is your submitted solution. Its program logic is unchanged.
# EXAM TIP: read it top to bottom. Python executes top-level statements immediately.
# Look at solution.py for the reusable, beginner-friendly rewrite.
# Input files for this challenge are in the adjacent data/ folder.


# EXPLAINED: Import a Python library so this script can use its functions.
import hashlib
import json
import socket
from datetime import datetime, timezone, timedelta


HOST = "cns-test.idlab.uantwerpen.be"
PORT = 50003

# Hypothesis: first 4 bytes of SHA-256
FINGERPRINT_BYTES = 4


# EXPLAINED: Define a reusable function; its body runs when the function is called.
def canonicalize(payment):
    # EXPLAINED: Serialize Python data to JSON. Byte-for-byte format can matter for hashes.
    return json.dumps(
        payment,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")


def find_collision():
    # Use a timestamp safely within the previous minute.
    timestamp = (
        datetime.now(timezone.utc) - timedelta(seconds=10)
    ).isoformat()

    payment = {
        "reference": "PAY-0",
        "from_account": "SIM-ALICE",
        "to_account": "SIM-BOB",
        "amount": 10,
        "currency": "EUR",
        "timestamp": timestamp
    }

    fingerprints = {}

    # EXPLAINED: Repeat the next indented lines for each possible value.
    for i in range(300_000):
        payment["reference"] = f"PAY-{i}"

        canonical = canonicalize(payment)

        # EXPLAINED: Calculate a cryptographic digest of the bytes supplied here.
        full_hash = hashlib.sha256(canonical).digest()
        fingerprint = full_hash[:FINGERPRINT_BYTES]

        # EXPLAINED: Run the indented block only when this condition is true.
        if fingerprint in fingerprints:
            previous = fingerprints[fingerprint]

            if previous != canonical:
                print("\nCollision found!")
                print("Fingerprint:", fingerprint.hex())
                print("Payment 1:", previous.decode())
                print("Payment 2:", canonical.decode())

                return previous, canonical
        else:
            fingerprints[fingerprint] = canonical

    return None, None

def main():
    payment1, payment2 = find_collision()

    if payment1 is None:
        print("No collision found. Trying again...")
        payment1, payment2 = find_collision()

    if payment1 is None:
        print("Could not find a collision.")
        return


if __name__ == "__main__":
    main()
