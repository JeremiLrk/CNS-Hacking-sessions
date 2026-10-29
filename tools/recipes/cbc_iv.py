"""CBC first-block modification, if IV is editable and no authentication protects it.
Formula: IV_new = IV_old XOR P_old XOR P_wanted.
Run python3 -m tools.recipes.cbc_iv --help
"""
import argparse

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--iv',required=True,help='16-byte IV, hex encoded')
    p.add_argument('--old',required=True)
    p.add_argument('--new',required=True)
    a=p.parse_args()
    iv=bytes.fromhex(a.iv);old=a.old.encode();new=a.new.encode()
    if len(iv)!=16 or len(old)!=16 or len(new)!=16:
        p.error('IV, old and new plaintext must each contain 16 bytes')
    forged=bytes(x^y^z for x,y,z in zip(iv,old,new))
    print('New IV hex:',forged.hex())
    print('Leave ciphertext unchanged.')
if __name__=='__main__':main()
