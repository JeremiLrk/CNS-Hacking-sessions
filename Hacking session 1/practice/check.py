"""CNS OFFLINE FLAG CHECKER: run `python check.py C01 "YOUR_ANSWER"`.

This file contains NO challenge solutions or plaintext flags.
For normal exercises the correct answer is used to unlock reward.bin.
The special collision exercise (H07) validates your collision proof directly.
"""
from pathlib import Path
import hashlib, struct, argparse, re, sys
BASE=Path(__file__).resolve().parent
CHALLENGE_FOLDERS = {'S08': 'round_01/exercise_01_stream_S08', 'B03': 'round_01/exercise_02_block_B03', 'H02': 'round_01/exercise_03_hash_H02', 'M04': 'round_01/exercise_04_mac_M04', 'S06': 'round_02/exercise_01_stream_S06', 'B04': 'round_02/exercise_02_block_B04', 'H06': 'round_02/exercise_03_hash_H06', 'M03': 'round_02/exercise_04_mac_M03', 'S05': 'round_03/exercise_01_stream_S05', 'B10': 'round_03/exercise_02_block_B10', 'H07': 'round_03/exercise_03_hash_H07', 'M02': 'round_03/exercise_04_mac_M02'}

def mask(key,n):
    result=bytearray(); counter=0
    while len(result)<n:
        result.extend(hashlib.sha256(key+counter.to_bytes(4,'big')).digest())
        counter+=1
    return result[:n]

def check(cid,answer):
    cid=cid.upper()
    if cid=='H07':
        try:
            xa,xb=answer.split(':',1)
            a=bytes.fromhex(xa);b=bytes.fromhex(xb)
            assert a and b and a!=b
            assert hashlib.sha256(a).digest()[:3] == hashlib.sha256(b).digest()[:3]
        except (ValueError,AssertionError):
            return 'Not a valid 24-bit SHA256 collision. Check both hex messages.'
        fp=hashlib.sha256(a+b'|'+b).hexdigest()[:12]
        return f'CORRECT! cns{{h07_birthday_{fp}}}'
    if cid=='M07':
        return 'M07 is an interactive HTTP challenge. Start its replay_service.py and solve it through /challenge and /gate.'
    reward=BASE/CHALLENGE_FOLDERS.get(cid, 'missing')/'reward.bin'
    if not reward.exists():return 'Unknown exercise ID.'
    data=reward.read_bytes()
    secret=answer.encode('utf-8')
    m=mask(secret,len(data))
    plain=bytes(x^y for x,y in zip(data,m))
    try:out=plain.decode('ascii')
    except UnicodeDecodeError:return 'Not correct yet. Try a different answer.'
    if re.fullmatch(r'cns\{'+cid.lower()+r'_[0-9a-f]{10}\}',out):
        return 'CORRECT! '+out
    return 'Not correct yet. Try a different answer.'

if __name__=='__main__':
    parser=argparse.ArgumentParser(description='Offline CNS practice flag checker')
    parser.add_argument('challenge',help='Example: C01, S05, B10, H06, M03')
    parser.add_argument('answer',nargs='?',help='Exact answer as a string')
    parser.add_argument('--file',help='Read exact answer from UTF-8 text file; remove only final newline')
    a=parser.parse_args()
    if a.file:
        val=Path(a.file).read_text(encoding='utf-8').rstrip('\r\n')
    elif a.answer is not None:
        val=a.answer
    else:parser.error('Provide an answer or --file PATH')
    print(check(a.challenge,val))
