# H07 — Birthday party in 24 bits

**Category:** Hashing  
**Difficulty:** 4 / 5  
**Relevant slides:** Part 3 pp. 11–16  
**Suggested tools:** Python 3.11+; installed CNS library helpful

## Mission

The badge system stores only the first **24 bits** (3 bytes) of SHA-256. Find TWO DIFFERENT messages (arbitrary bytes, represented as lowercase hex) with the same 3-byte truncated digest. Submit exactly `first_message_hex:second_message_hex`. Both strings must be nonempty and represent different byte sequences. This is a **collision attack**, not finding the preimage of one chosen digest. The checker will generate a valid `cns{...}` flag from your collision pair.

## Provided files

- `rules.txt`

## How to submit

Find the requested **answer** (not the flag) and run at the top of the lab folder:

```powershell
python check.py H07 "YOUR_ANSWER"
```

If the answer contains JSON, spaces or PowerShell-special characters, save it to a UTF-8 text file and use:

```powershell
python check.py H07 --file answer.txt
```

The checker decrypts `reward.bin` and prints a `cns{...}` flag **only for the correct answer**. It does not tell you which attack to use. Read `HINTS.md` only if needed.
