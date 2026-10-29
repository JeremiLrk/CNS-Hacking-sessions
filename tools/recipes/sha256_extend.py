"""SHA256(secret || message) length extension, NOT HMAC.
Run python3 -m tools.recipes.sha256_extend --help
The output message includes nonprintable glue padding; submit actual bytes.
"""
import argparse
from tools.hash.sha256_length_extension import sha256_length_extension

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--digest',required=True,help='Known SHA256(secret || old_message) digest')
    p.add_argument('--message',required=True,help='Known original message text')
    p.add_argument('--append',required=True,help='Desired suffix to add')
    p.add_argument('--secret-length',type=int,required=True)
    a=p.parse_args()
    forged,digest=sha256_length_extension(a.digest,a.message.encode(),a.append.encode(),a.secret_length)
    print('Forged message hex:',forged.hex())
    print('Forged digest hex:',digest)
    print('Answer pair:',forged.hex()+':'+digest)
if __name__=='__main__':main()
