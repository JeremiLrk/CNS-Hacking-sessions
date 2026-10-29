# S05 — ChaCha20 counter offset

**Category:** Stream  
**Difficulty:** 5 / 5  
**Relevant slides:** Part 2 pp. 46–58  
**Suggested tools:** Python 3.11+; installed CNS library helpful

## Mission

Two ChaCha20 messages share key and 8-byte nonce. The known public ciphertext started at 64-byte-block counter **0**; the secret ciphertext started at block counter **3**. Find the secret `CODE=` using the known plaintext. A simple `P1 XOR C1 XOR C2` starting at byte zero will fail! The challenge uses a 64-byte ChaCha block, and all given inputs are raw bytes/hex.

## Provided files

- `public_plain.bin`
- `public_cipher.hex`
- `private_cipher.hex`
- `config.txt`

## How to submit

Find the requested **answer** (not the flag) and run at the top of the lab folder:

```powershell
python check.py S05 "YOUR_ANSWER"
```

If the answer contains JSON, spaces or PowerShell-special characters, save it to a UTF-8 text file and use:

```powershell
python check.py S05 --file answer.txt
```

The checker decrypts `reward.bin` and prints a `cns{...}` flag **only for the correct answer**. It does not tell you which attack to use. Read `HINTS.md` only if needed.
