# CNS Hacking Sessions — EXAM TOOLKIT

> **START HERE during the hacking session.** Fast navigation, working command examples, known pitfalls, old exercises, and offline practice. Only use on course challenges or systems you are authorized to test.

## 🚀 30-second start

```bash
git clone https://github.com/JeremiLrk/CNS-Hacking-sessions.git
cd CNS-Hacking-sessions
python3 --version
python3 smoke_test.py             # Check Python basics + CLI tools
python3 -m tools.recipes.xor_reuse --help
```

**Quick system check:** `python3 smoke_test.py` should print `[PASS]` for basic byte operations, SHA-256, XOR and five CLI recipe help commands. It does not test live challenge servers or optional packages.

**Windows PowerShell:** use `py` or `python` instead of `python3` if needed.

Optional crypto packages (AES/DES/Salsa20):
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Windows activation: `.venv\Scripts\Activate.ps1`. Many built-in Python examples do not need any pip packages.

## 📚 Choose your chapter

| Chapter | What to recognize | Start |
|---|---|---|
| **1 — Introduction** | Caesar, Vigenère, substitution, Enigma, XOR, bytes/hex, network commands | [Chapter 1 quick guide](docs/01_INTRODUCTION.md) |
| **2 — Symmetric Encryption** | OTP reuse, Salsa20/ChaCha20, AES, DES, ECB, CBC, counter/nonce, bitflips | [Chapter 2 quick guide](docs/02_SYMMETRIC_ENCRYPTION.md) |
| **3 — Hash Functions** | SHA, hash dictionary, collision, HMAC, signed JSON, length extension, JWT | [Chapter 3 quick guide](docs/03_HASH_FUNCTIONS.md) |

**Most useful single page:** [ONE-PAGE EXAM CHEATSHEET](docs/EXAM_CHEATSHEET.md)

**Detailed explanation and requirements:** [Attack Playbook](docs/ATTACK_PLAYBOOK.md)

## 🔎 I see this in the challenge… what now?

| Clue | Technique | Exact command / file |
|---|---|---|
| `616263` | Hex → bytes | `bytes.fromhex("616263")` |
| Caesar / shift | Try all 26 shifts | [classical_ciphers.py](tools/basics/classical_ciphers.py) |
| Repeating XOR key | XOR and repeat key | [xor_and_stream_basics.py](tools/basics/xor_and_stream_basics.py) |
| Known plaintext + same stream key/nonce/counter | Recover keystream | `python3 -m tools.recipes.xor_reuse --help` |
| Change encrypted amount/role in stream cipher | XOR bitflip (no MAC) | `python3 -m tools.recipes.stream_bitflip --help` |
| Repeated 16-byte AES blocks | ECB analysis | [aes_modes.py](tools/block/aes_modes.py) |
| Editable CBC IV | CBC first-block modification | `python3 -m tools.recipes.cbc_iv --help` |
| DES key mostly known | Brute force missing key bytes | [des_small_key_solver.py](tools/block/des_small_key_solver.py) |
| Double encryption with small keys | Meet-in-the-middle | [double_aes_mitm.py](tools/block/double_aes_mitm.py) |
| Password candidates + hash | Dictionary check | `python3 -m tools.recipes.hash_dictionary --help` |
| Truncated digest | Birthday collision | [hash_functions.py](tools/hash/hash_functions.py) |
| `SHA256(secret || message)` MAC | Length extension if applicable | [sha256_length_extension.py](tools/hash/sha256_length_extension.py) |
| Signed JSON or JWT | Inspect bytes, parser, algorithm | [json_parser_tricks.py](tools/web/json_parser_tricks.py), [jwt_none.py](tools/recipes/jwt_none.py) |
| Wireshark RTSP Digest | Offline candidate validation | [rtsp_digest_solver.py](tools/web/rtsp_digest_solver.py) |

**These are clues, not guarantees.** Check attack preconditions in the linked guides.

## 🐍 Copy/paste Python essentials

**1. Hex, UTF-8, Base64**
```python
import base64
raw = bytes.fromhex("68656c6c6f")
print(raw)                        # b'hello'
print(raw.decode("utf-8"))         # hello
print(raw.hex())                   # 68656c6c6f
print(base64.b64decode("aGVsbG8=")) # b'hello'
```

**2. XOR bytes**
```python
def xor(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))

print(xor(bytes.fromhex("4142"), bytes.fromhex("0101")).hex())  # 4043
# zip stops at the SHORTEST input. Check lengths if full coverage is required.
```

**3. Reused stream known-plaintext example**
```python
known_plain = b"hello"
known_cipher = bytes.fromhex("09070f0d0e")  # demo ciphertext
other_cipher = bytes.fromhex("160d130d05")
keystream = xor(known_plain, known_cipher)
print(xor(other_cipher, keystream))
# Works only when the SAME keystream bytes align; not a general cipher break.
```

**4. Hash raw bytes vs hex string**
```python
import hashlib
data = b"password"
first = hashlib.sha256(data)
print(first.hexdigest())                               # hex representation
print(hashlib.sha256(first.digest()).hexdigest())       # SHA256(raw digest)
print(hashlib.sha256(first.hexdigest().encode()).hexdigest()) # SHA256(hex text)
# These two double-hashes are different!
```

**5. Read/write real binary data**
```python
from pathlib import Path
cipher = Path("cipher.bin").read_bytes()
print(len(cipher), cipher[:16].hex())
Path("output.bin").write_bytes(cipher)
```

## 🧰 Ready-to-run CLI recipes

Always run from the **repository root** (directory containing `tools/`).

**Stream keystream reuse:**
```bash
python3 -m tools.recipes.xor_reuse --known "hello" --known-cipher 09070f0d0e --secret-cipher 160d130d05
```

**Modify unauthenticated stream ciphertext:**
```bash
python3 -m tools.recipes.stream_bitflip --cipher-hex 010203040506 --offset 1 --old abc --new xyz
```

**Change CBC first plaintext block via editable IV:**
```bash
python3 -m tools.recipes.cbc_iv --iv 00000000000000000000000000000000 --old 'role=user;id=001' --new 'role=root;id=001'
```
Both text values must be **exactly 16 UTF-8 bytes**; inspect `--help` if using your own values.

**Offline dictionary lookup:**
```bash
python3 -m tools.recipes.hash_dictionary --wordlist past-exercises/04_count_letters/data/wordlist.txt --target YOUR_SHA256_HEX --mode sha256
```
Use `--help` to see the alternate modes.

**JWT lab validator demonstration:**
```bash
python3 -m tools.recipes.jwt_none --token 'HEADER.PAYLOAD.SIGNATURE' --role admin
```
This is only a valid exploit against an incorrectly configured validator.

## 🗂️ Original solved exercises

All **17 original CNS challenge solutions** are in [past-exercises/](past-exercises/), each with `solution.py`; some also have `original.py`.

| # | Folder | Main topic |
|---|---|---|
| 01–04 | [Caesar](past-exercises/01_caesar/), [Switcheroo](past-exercises/02_switcheroo/), [Vigenère](past-exercises/03_french_vigenere/), [Letter frequency](past-exercises/04_count_letters/) | Classical |
| 05–07 | [XOR](past-exercises/05_dutch_xor/), [Enigma](past-exercises/06_enigma/), [Weak PRNG](past-exercises/07_replanting/) | Intro / stream |
| 08–12 | [Secure Bank](past-exercises/08_secure_bank/), [DES](past-exercises/09_des_iotdev/), [Nonce reuse](past-exercises/10_noncense/), [Double AES](past-exercises/11_aes2/), [Secure Bank 2](past-exercises/12_secure_bank_2/) | Symmetric |
| 13–17 | [Better hash](past-exercises/13_better_hash/), [Space race](past-exercises/14_space_race/), [Security cam](past-exercises/15_security_cam/), [HMAC JSON](past-exercises/16_hmac_json/), [JWT](past-exercises/17_jwt/) | Hash / authentication |

## 🧪 Practice exam: 12 exercises, 3 rounds

| Round | Stream | Block | Hash | MAC / Auth |
|---|---|---|---|---|
| 1 | S08 nonce reuse | B03 ECB splicing | H02 double SHA | M04 signed JSON |
| 2 | S06 PRNG | B04 CBC IV | H06 length extension | M03 JWT |
| 3 | S05 ChaCha counter | B10 double AES | H07 birthday collision | M02 RTSP Digest |

Start in [practice/](practice/). Read each `challenge.md` **before** `solution.py`.

Example checker, from repo root:
```bash
python3 practice/check.py S08 'YOUR_ANSWER'
python3 practice/check.py H02 'YOUR_ANSWER'
# For answers with quotation marks/special characters:
python3 practice/check.py S08 --file answer.txt
```
Checker returns a flag only on correct input. **The flag is not the answer you submit to the checker.**

## ⚠️ Exam gotchas

- `hex` and Base64 are *encodings*, not encryption.
- `SHA256(data)` is not reversible; search candidates if a weak password is suspected.
- In stream-like encryption, same **key AND nonce/counter alignment** is required to reuse keystream.
- CBC IV bitflips affect plaintext block **1**; they are not the same as stream bitflips.
- Ciphertext authentication (MAC/AEAD) normally detects manipulation.
- AES block size is always **16 bytes**, regardless of key length.
- Do not mix `bytes` and `str`; encode/decode deliberately.
- Do not blindly assume every script works against a live service: endpoints, availability, keys and challenge parameters may change.
- Try your local script with known test inputs **before** using it in an exam.

## More support

- [Terminal and Ubuntu](docs/UBUNTU_TERMINAL.md)
- [Python syntax for beginners](docs/PYTHON_BASICS.md)
- [Attack playbook](docs/ATTACK_PLAYBOOK.md)
- [Exam cheatsheet](docs/EXAM_CHEATSHEET.md)

Educational course lab use only. Not an official UAntwerpen publication.
