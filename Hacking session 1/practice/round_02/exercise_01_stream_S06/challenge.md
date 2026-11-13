# S06 — Toy PRNG state recovery

**Category:** Stream  
**Difficulty:** 4 / 5  
**Relevant slides:** Part 2 pp. 37–39  
**Suggested tools:** Python 3.11+; installed CNS library helpful

## Mission

A broken stream cipher uses a 16-bit linear congruential generator. Each byte is taken from the **high byte** of the new state after stepping. Parameters and the first **34 plaintext bytes** are available, but seed is unknown. Brute force the 16-bit seed, validate with the known header, and decrypt the rest to recover `PRIVATE ACCESS=`. Submit the access value.

## Provided files

- `cipher.hex`
- `public_prefix.txt`
- `generator.txt`

## How to submit

Find the requested **answer** (not the flag) and run at the top of the lab folder:

```powershell
python check.py S06 "YOUR_ANSWER"
```

If the answer contains JSON, spaces or PowerShell-special characters, save it to a UTF-8 text file and use:

```powershell
python check.py S06 --file answer.txt
```

The checker decrypts `reward.bin` and prints a `cns{...}` flag **only for the correct answer**. It does not tell you which attack to use. Read `HINTS.md` only if needed.
