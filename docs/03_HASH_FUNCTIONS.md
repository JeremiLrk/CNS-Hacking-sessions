# CHAPTER 3 — Hash Functions / Authentication

[HOME](../README.md) · [EXAM CHEATSHEET](EXAM_CHEATSHEET.md)

## Identify the situation

| Clue | Technique | Check first |
|---|---|---|
| Password and SHA digest | Wordlist/dictionary | Encoding, salt, rounds, hash order |
| Double SHA | Hash raw bytes vs hex text | Which exact bytes are hashed twice? |
| Digest truncated to t bits | Birthday collision | ~2^(t/2) trials for *collision* |
| SHA256(secret || message) | Length extension | Vulnerable Merkle-Damgård secret-prefix MAC |
| HMAC(key,message) | Proper keyed MAC | Not the same length-extension flaw |
| Signed JSON | Parser mismatch | Exactly which bytes are authenticated? |
| JWT `alg` | Signature validation flaw | Only if validator incorrectly trusts it |

## Code: hash and double hash

```python
import hashlib
data = b"hello"
first = hashlib.sha256(data)
print(first.hexdigest())                                     # plain SHA256
print(hashlib.sha256(first.digest()).hexdigest())             # raw twice
print(hashlib.sha256(first.hexdigest().encode()).hexdigest()) # hex text twice
```

## Code: wordlist

```python
import hashlib
target = "REPLACE_WITH_HASH"
with open("candidates.txt","rb") as f:
    for line in f:
        word = line.rstrip(b"\r\n")
        if hashlib.sha256(word).hexdigest() == target:
            print("FOUND:",word)
            break
```

## Code: birthday collision on a SHORT hash

```python
import hashlib
seen = {}
for n in range(200000):
    msg = str(n).encode()
    h = hashlib.sha256(msg).digest()[:3]  # 24-bit demo only
    if h in seen and seen[h] != msg:
        print(seen[h].hex(),msg.hex(),h.hex())
        break
    seen[h] = msg
```

## HMAC is not plain SHA(secret + message)

```python
import hmac, hashlib
tag = hmac.new(b"key", b"message", hashlib.sha256).hexdigest()
print(tag)
```

## Relevant files

[Hash tools](../tools/hash/hash_functions.py) · [HMAC basics](../tools/hash/hmac_basics.py) · [Length extension](../tools/hash/sha256_length_extension.py) · [JSON parser](../tools/web/json_parser_tricks.py) · [JWT](../tools/web/jwt_for_beginners.py)

Previous exercises: [Better Hash](../past-exercises/13_better_hash/solution.py) · [Space Race](../past-exercises/14_space_race/solution.py) · [Security Camera](../past-exercises/15_security_cam/solution.py) · [HMAC JSON](../past-exercises/16_hmac_json/solution.py) · [JWT](../past-exercises/17_jwt/solution.py)

Practice [H02](../practice/round_01/exercise_03_hash_H02/challenge.md) · [H06](../practice/round_02/exercise_03_hash_H06/challenge.md) · [H07](../practice/round_03/exercise_03_hash_H07/challenge.md)
