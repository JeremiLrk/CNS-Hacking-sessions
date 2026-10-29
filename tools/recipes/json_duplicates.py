"""Show why differently configured JSON parsers can disagree on duplicate keys.
Run python3 -m tools.recipes.json_duplicates --help
Only applies to applications whose verifier and authorizer parse differently.
"""
import argparse,json

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--key',default='role')
    p.add_argument('--first',default='admin')
    p.add_argument('--last',default='user')
    a=p.parse_args()
    key=json.dumps(a.key);first=json.dumps(a.first);last=json.dumps(a.last)
    raw='{'+f'{key}:{first},{key}:{last}'+'}'
    print('Raw JSON:',raw)
    print('Python parsed (last wins):',json.loads(raw))
    print('A first-wins parser may see:',a.first)
    print('Do not turn the raw request into a Python dictionary before sending.')
if __name__=='__main__':main()
