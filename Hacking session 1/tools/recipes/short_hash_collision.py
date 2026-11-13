"""Birthday collision on first N bytes of SHA-256. N=3 for 24-bit demo.
IMPORTANT: never claim this is an attack on the full SHA-256 hash.
Run python3 -m tools.recipes.short_hash_collision --help
"""
import argparse,hashlib

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--prefix-bytes',type=int,default=3)
    p.add_argument('--max-attempts',type=int,default=200000)
    a=p.parse_args()
    if not 1<=a.prefix_bytes<=4:p.error('This educational script limits prefix size to 1..4 bytes')
    seen={}
    for i in range(a.max_attempts):
        raw=i.to_bytes(8,'big')
        prefix=hashlib.sha256(raw).digest()[:a.prefix_bytes]
        old=seen.get(prefix)
        if old is not None and old!=raw:
            print('Collision prefix:',prefix.hex())
            print('Message 1:',old.hex())
            print('Message 2:',raw.hex())
            print('Submit as:',old.hex()+':'+raw.hex())
            return
        seen[prefix]=raw
    print('No collision before limit; try raising --max-attempts')
if __name__=='__main__':main()
