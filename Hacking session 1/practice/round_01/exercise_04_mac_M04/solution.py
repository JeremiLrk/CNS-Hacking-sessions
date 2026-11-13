"""M04: HMAC is sound; two JSON parsers disagree about duplicate keys.

Verifier uses JSON.loads: last duplicate key wins. So it sees viewer.
Authorization uses first-key-wins: it sees admin.
The secret HMAC key is never recovered or modified.
"""
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent

def main():
    original=json.loads((HERE/'signed_request.json').read_text())
    print('Captured signature:',original['x_signature'])
    # Do not use a Python dict here! Dicts cannot represent duplicate keys.
    # We need RAW JSON text, with two "access" entries in nested request.
    forged='{"action":"read","request":{"region":"north","access":"admin","access":"viewer"}}'
    # Demonstrate the parser used by the verifier.
    parsed=json.loads(forged)
    print('Verifier sees:',parsed['request']['access'])
    print('Authorizer (first-key-wins) sees: admin')
    print('SUBMIT:',forged)

if __name__=='__main__':
    main()
