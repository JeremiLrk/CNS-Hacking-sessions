"""Try words against given hash; supports raw vs hex second-hash representations.
This is for offline wordlists and lab-provided hash values.
Run python3 -m tools.recipes.hash_dictionary --help
"""
import argparse,hashlib

def calculate(word,mode):
    first=hashlib.sha256(word)
    if mode=='sha256':return first.hexdigest()
    if mode=='sha256-raw-twice':return hashlib.sha256(first.digest()).hexdigest()
    if mode=='sha256-hex-text-twice':return hashlib.sha256(first.hexdigest().encode()).hexdigest()
    if mode=='md5':return hashlib.md5(word).hexdigest()
    if mode=='sha1':return hashlib.sha1(word).hexdigest()
    raise ValueError('Unexpected mode')

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--wordlist',required=True)
    p.add_argument('--target',required=True,help='Expected digest as hex')
    p.add_argument('--mode',choices=['sha256','sha256-raw-twice','sha256-hex-text-twice','md5','sha1'],default='sha256')
    a=p.parse_args()
    with open(a.wordlist,'rb') as f:
        for raw in f:
            word=raw.rstrip(b'\r\n')
            if calculate(word,a.mode)==a.target.lower():
                print('Found:',word.decode('utf-8',errors='replace'))
                return
    print('No match found in this list')
if __name__=='__main__':main()
