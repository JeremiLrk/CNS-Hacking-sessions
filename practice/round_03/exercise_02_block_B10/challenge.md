# B10 — Double AES demo that still fails

**Category:** Block  
**Difficulty:** 5 / 5  
**Relevant slides:** Part 2 pp. 73–77 + meet-in-the-middle [EXTRA]  
**Suggested tools:** cryptography or PyCryptodome

## Mission

A developer encrypted each 16-byte block twice: `C = AES_ECB(K2, AES_ECB(K1, P))`. Each AES-128 key is formed from a 12-bit integer in a 2-byte BIG ENDIAN representation, followed by 14 zero bytes. You have **two known plaintext/ciphertext block pairs**. Discover both small integers using a meet-in-the-middle attack (not 2^24 naive pairs). Submit the answer exactly `k1_decimal,k2_decimal` with no spaces. Use the second pair to reject wrong matches.

## Provided files

- `pairs.json`

## How to submit

Find the requested **answer** (not the flag) and run at the top of the lab folder:

```powershell
python check.py B10 "YOUR_ANSWER"
```

If the answer contains JSON, spaces or PowerShell-special characters, save it to a UTF-8 text file and use:

```powershell
python check.py B10 --file answer.txt
```

The checker decrypts `reward.bin` and prints a `cns{...}` flag **only for the correct answer**. It does not tell you which attack to use. Read `HINTS.md` only if needed.
