"""M02: crack a captured RTSP Digest password (qop=auth variant).

The older RTSP exercise had a simpler formula. Here you MUST include
nonce-count, client-nonce and qop in the correct order, else none match.
Only test the supplied educational candidate wordlist.
"""
import hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent

# Values copied from the provided lab capture.
USER='operator'
REALM='DockRTSP'
METHOD='DESCRIBE'
URI='rtsp://camera.lab.local:8554/stream'
NONCE='f838de8a694f396e768f2ce80e9b2e02'
NC='00000001'
CNONCE='a91367b5b24f0767'
QOP='auth'
EXPECTED='27788f27b8aee69552d30e7e0e8721a8'

def md5_hex(value):
    return hashlib.md5(value).hexdigest()

def response_for(password_bytes):
    # HA1 = MD5(username : realm : password)
    first_part=f'{USER}:{REALM}:'.encode()+password_bytes
    ha1=md5_hex(first_part)
    # HA2 = MD5(method : URI)
    ha2=md5_hex(f'{METHOD}:{URI}'.encode())
    # Full qop=auth formula (six colon-separated fields).
    response=f'{ha1}:{NONCE}:{NC}:{CNONCE}:{QOP}:{ha2}'
    return md5_hex(response.encode())

def main():
    for line in (HERE/'passwords.txt').read_bytes().splitlines():
        password=line.rstrip(b'\r\n')
        if response_for(password)==EXPECTED:
            print('SUBMIT:',password.decode('utf-8',errors='replace'))
            return
    print('No matching password found')

if __name__=='__main__':
    main()
