"""Edit an unauthenticated stream ciphertext using known old and desired plaintext.
Run python3 -m tools.recipes.stream_bitflip --help
Same length only; choose offsets relative to the ciphertext, NOT nonce prefix.
"""
import argparse

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--cipher-hex',required=True)
    p.add_argument('--offset',type=int,required=True)
    p.add_argument('--old',required=True,help='Current known plaintext at the given byte offset')
    p.add_argument('--new',required=True,help='Desired plaintext at the same position')
    a=p.parse_args(); cipher=bytearray.fromhex(a.cipher_hex)
    old=a.old.encode();new=a.new.encode()
    if len(old)!=len(new):p.error('Old and new UTF-8 texts differ in BYTE length')
    if a.offset<0 or a.offset+len(old)>len(cipher):p.error('Outside ciphertext')
    for i in range(len(old)):
        cipher[a.offset+i] ^= old[i] ^ new[i]
    print('Modified ciphertext hex:',cipher.hex())
    print('Note: Authentication tags normally reject such modifications.')
if __name__=='__main__':main()
