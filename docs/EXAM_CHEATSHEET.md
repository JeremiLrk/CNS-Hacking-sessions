# CNS — FAST EXAM CHEATSHEET

**When stuck:** read the input format → identify algorithm/mode → find known data → verify required assumptions → test small → inspect bytes/hex → check results.

| Given | Suspect | Need | Formula |
|---|---|---|---|
| Shifted alphabet | Caesar | Alphabet | Try 26 shifts |
| Repeating short XOR key | Repeating XOR | Key or known text | `P[i] = C[i] ^ K[i % len(K)]` |
| Two stream ciphertexts | Key/nonce reuse | Identical keystream alignment | `C1 ^ C2 = P1 ^ P2` |
| Known P1,C1 and C2 | Known plaintext stream | Same keystream | `P2 = C2 ^ P1 ^ C1` |
| Alter plaintext in XOR stream | Bit flipping | Old/new bytes, same length, no MAC | `C' = C ^ Pold ^ Pnew` |
| Editable CBC IV | CBC first block | Old/new P1, no auth | `IV' = IV ^ P1 ^ P1'` |
| Repeated 16-byte blocks | ECB | Same key/mode | Compare 16-byte blocks |
| Double encryption / tiny keys | Meet in the middle | Known plaintext/ciphertext pairs | `E_K1(P) = D_K2(C)` |
| Short digest | Truncated-hash collision | t-bit hash | ~`2^(t/2)` attempts |
| Password hash | Dictionary attack | Target digest, candidates | `hash(candidate)==target` |
| `hash(secret||message)` | Length extension | Vulnerable iterative hash, secret length guess | Forge suffix with padding |
| HMAC | Keyed authentication | Secret key | Not susceptible to ordinary length extension |

## Must-know code

```python
import hashlib, base64, json
from pathlib import Path
raw = bytes.fromhex("636e73")    # b'cns'
text = raw.decode()
hex_text = raw.hex()
encoded = text.encode()
decoded = base64.b64decode("Y25z")
digest_hex = hashlib.sha256(raw).hexdigest()
digest_raw = hashlib.sha256(raw).digest()
data = Path("input.bin").read_bytes()
Path("output.bin").write_bytes(data)
```

```python
def xor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))
# zip silently truncates: inspect len(a), len(b)!
```

```python
# repeated-key XOR decryption (if key known)
cipher = bytes.fromhex("010203")
key = b"abc"
plain = bytes(c ^ key[i % len(key)] for i,c in enumerate(cipher))
print(plain)
```

```python
# inspect ECB blocks and repeats
from collections import Counter
cipher = bytes.fromhex("00" * 32) # REPLACE with challenge ciphertext
blocks = [cipher[i:i+16] for i in range(0,len(cipher),16)]
print(Counter(blocks).most_common())
```

```python
# SHA-256 password check
from hashlib import sha256
candidate = b"password"
target = "REPLACE_WITH_TARGET_HASH"
print(sha256(candidate).hexdigest() == target)
```

## Command reference

```bash
pwd
ls -la
file input.bin
xxd -l 64 input.bin
python3 script.py
python3 -m tools.recipes.xor_reuse --help
python3 -m tools.recipes.stream_bitflip --help
python3 -m tools.recipes.cbc_iv --help
python3 -m tools.recipes.hash_dictionary --help
nc HOST PORT
curl -i http://HOST:PORT/
```

**Never assume** the service is available or the port is open. For details open [ATTACK_PLAYBOOK.md](ATTACK_PLAYBOOK.md).


## Past-exercise lookup

| If you need… | Check this previous exercise |
|---|---|
| Classical cipher or XOR | [01 Caesar](../past-exercises/01_caesar/solution.py), [03 Vigenère](../past-exercises/03_french_vigenere/solution.py), [05 XOR](../past-exercises/05_dutch_xor/solution.py), [06 Enigma](../past-exercises/06_enigma/solution.py) |
| Stream bitflipping | **[08 Secure Bank](../past-exercises/08_secure_bank/solution.py)** |
| Reused nonce/keystream | [10 Noncense](../past-exercises/10_noncense/solution.py) |
| Weak PRNG | [07 Replanting](../past-exercises/07_replanting/solution.py) |
| Small DES keyspace | [09 DES IoT Device](../past-exercises/09_des_iotdev/solution.py) |
| Double AES | [11 AES2](../past-exercises/11_aes2/solution.py) |
| Weak hashes | [13 Better Hash](../past-exercises/13_better_hash/solution.py) |
| HTTP/RTSP Digest | [15 Security Cam](../past-exercises/15_security_cam/solution.py) |
| Signed JSON/HMAC | [16 HMAC JSON](../past-exercises/16_hmac_json/solution.py) |
| JWT | [17 JWT](../past-exercises/17_jwt/solution.py) |
