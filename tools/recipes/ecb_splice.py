"""Replace exactly one AES-ECB ciphertext block with a donor block from SAME key.
Run python3 -m tools.recipes.ecb_splice --help
"""
import argparse
BLOCK=16

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--cipher',required=True,help='Original ciphertext as hex')
    p.add_argument('--block-index',type=int,required=True,help='Zero-based block to replace')
    p.add_argument('--replacement',required=True,help='Exactly 16 ciphertext bytes as hex')
    a=p.parse_args()
    original=bytes.fromhex(a.cipher);donor=bytes.fromhex(a.replacement)
    if len(original)%16:p.error('Ciphertext length must be multiple of 16')
    if len(donor)!=16:p.error('Donor must contain exactly 16 bytes')
    if a.block_index<0 or a.block_index>=len(original)//16:p.error('Bad block index')
    start=a.block_index*16
    forged=original[:start]+donor+original[start+16:]
    print('Forged ciphertext hex:',forged.hex())
if __name__=='__main__':main()
