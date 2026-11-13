"""SECURE BANK 2 — find two DIFFERENT payments with the SAME short fingerprint.

WHEN TO TRY: The application stores only part of a secure hash (for example
4 bytes of SHA-256). The full SHA-256 might be strong, but a 4-byte prefix
has only 2^32 possible values. The birthday effect allows collisions in
roughly 2^16 random/varied records, not 2^32.

The challenge did NOT specify exactly how fingerprint is shortened.
Your submitted code used the first 4 bytes. That code was successful for your lab exercise.
The assistant did not reconnect to the live server.

Every JSON field must match the challenge's validation rules.
"""

import hashlib
import json
import socket
from datetime import datetime, timedelta, timezone

HOST = "cns-test.idlab.uantwerpen.be"
PORT = 50003
FINGERPRINT_BYTES = 4  # Value from your successfully used script.


def canonical_json(payment):
    # Server's specified JSON format: sorted keys and NO extra spaces.
    text = json.dumps(payment, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return text.encode("utf-8")


def payment_template():
    # Two SIM accounts, amount exactly 10, EUR, ISO 8601 timestamp.
    return {
        "reference": "PAY-0",
        "from_account": "SIM-ALICE",
        "to_account": "SIM-BOB",
        "amount": 10,
        "currency": "EUR",
        "timestamp": (datetime.now(timezone.utc) - timedelta(seconds=10)).isoformat(),
    }


def find_collision(max_attempts=300000, fingerprint_bytes=FINGERPRINT_BYTES):
    payment = payment_template()
    seen = {}

    for counter in range(max_attempts):
        payment["reference"] = f"PAY-{counter}"
        current_json = canonical_json(payment)
        digest = hashlib.sha256(current_json).digest()
        small_fingerprint = digest[:fingerprint_bytes]

        if small_fingerprint in seen:
            old_json = seen[small_fingerprint]
            if old_json != current_json:
                return old_json, current_json, small_fingerprint
        else:
            seen[small_fingerprint] = current_json

    return None


def send_both_lines(first_json, second_json):
    # Only connect when intentionally running in your authorized CNS lab.
    # Both lines are sent in a single TCP connection.
    with socket.create_connection((HOST, PORT), timeout=8) as connection:
        connection.sendall(first_json + b"\n" + second_json + b"\n")
        connection.shutdown(socket.SHUT_WR)
        data = bytearray()
        while True:
            part = connection.recv(4096)
            if not part:
                break
            data.extend(part)
        return bytes(data)


def main():
    result = find_collision()
    if result is None:
        print("No collision yet; try changing the bound or guessed hash length.")
        return

    first, second, fingerprint = result
    print("Collision found on the first", FINGERPRINT_BYTES, "SHA-256 bytes.")
    print("Fingerprint:", fingerprint.hex())
    print("Payment record 1:", first.decode())
    print("Payment record 2:", second.decode())
    print("Send the two JSON strings as separate lines in the authorized lab.")
    # Uncomment ONLY on the authorized university VPN/lab:
    # print(send_both_lines(first, second).decode(errors="replace"))


if __name__ == "__main__":
    main()
