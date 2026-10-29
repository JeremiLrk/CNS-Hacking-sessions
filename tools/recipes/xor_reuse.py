"""Decrypt another stream-cipher ciphertext using a known plaintext and a reused keystream.
Run: python3 -m tools.recipes.xor_reuse --help
IMPORTANT: same key, nonce, counter START and plaintext alignment required.
"""
import argparse

def xor_prefix(a,b):
    # zip pairs one byte from each input and stops at the shortest.
    return bytes(left ^ right for left,right in zip(a,b))

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--known',required=True,help='Known plain text as ordinary UTF-8 string')
    p.add_argument('--known-cipher',required=True,help='Hex ciphertext for the known message')
    p.add_argument('--secret-cipher',required=True,help='Hex ciphertext for secret message')
    p.add_argument('--stream-offset',type=int,default=0,help='Byte offset into known keystream for secret counter; default zero')
    a=p.parse_args()
    known=a.known.encode()
    known_cipher=bytes.fromhex(a.known_cipher)
    secret_cipher=bytes.fromhex(a.secret_cipher)
    if len(known)!=len(known_cipher):
        p.error('Known plaintext and its ciphertext must have the same length.')
    keystream=xor_prefix(known,known_cipher)
    use=keystream[a.stream_offset:a.stream_offset+len(secret_cipher)]
    if len(use)<len(secret_cipher):
        p.error('Not enough known plaintext to cover the secret ciphertext at that offset.')
    answer=xor_prefix(secret_cipher,use)
    print('Decrypted (text):',answer.decode('utf-8',errors='replace'))
    print('Decrypted (hex):',answer.hex())

if __name__=='__main__': main()
