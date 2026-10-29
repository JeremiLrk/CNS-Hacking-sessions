"""H06: SHA-256 length extension on SHA256(secret || message).

This does NOT work against a correctly designed HMAC.
We need to know how many BYTES the secret occupies, not the secret bytes.
The challenge states 9..18 bytes. Build one candidate for every length.

Run from repo root: python3 -m practice.round_02.exercise_03_hash_H06.solution
or run directly: python3 practice/round_02/exercise_03_hash_H06/solution.py
"""
import json
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]  # the repository root
sys.path.insert(0,str(ROOT))
from tools.hash.sha256_length_extension import sha256_length_extension


def main():
    data=json.loads((HERE/'signed_request.json').read_text())
    message=data['original_message_ascii'].encode()
    known_digest=data['original_sha256_hex']
    extra=data['append_ascii'].encode()
    low,high=data['secret_length_range_inclusive']
    print('Try each of these candidates in practice/check.py H06 --file answer.txt')
    for secret_length in range(low,high+1):
        # The helper continues SHA-256 from a known digest, after adding
        # the glue padding. You never need to learn the secret key bytes.
        forged_message, forged_digest = sha256_length_extension(
            known_digest, message, extra, secret_length
        )
        answer=forged_message.hex()+':'+forged_digest
        print('GUESS LENGTH:',secret_length,'ANSWER:',answer)
        # A local reward checker can distinguish the correct key length.
        # For a real web service you would submit the candidate to its API.

if __name__=='__main__':
    main()
