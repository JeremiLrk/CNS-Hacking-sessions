# B04 — CBC first-block IV trick

**Category:** Block  
**Difficulty:** 4 / 5  
**Relevant slides:** Part 2 pp. 103–105  
**Suggested tools:** Python 3.11+; installed CNS library helpful

## Mission

The request starts with `access=guest;pad` in plaintext block 1, encrypted using AES-CBC. The server mistakenly allows an attacker to replace the **IV** without verifying authenticity. Change the IV so plaintext block 1 decrypts to exactly `access=admin;pad` (same length); do not edit the ciphertext. Submit the **new IV hex** (32 lowercase hex characters).

## Provided files

- `iv.hex`
- `cipher.hex`
- `original_block1.txt`

## How to submit

Find the requested **answer** (not the flag) and run at the top of the lab folder:

```powershell
python check.py B04 "YOUR_ANSWER"
```

If the answer contains JSON, spaces or PowerShell-special characters, save it to a UTF-8 text file and use:

```powershell
python check.py B04 --file answer.txt
```

The checker decrypts `reward.bin` and prints a `cns{...}` flag **only for the correct answer**. It does not tell you which attack to use. Read `HINTS.md` only if needed.
