# H02 — The digest of a digest

**Category:** Hashing  
**Difficulty:** 4 / 5  
**Relevant slides:** Part 3 pp. 5–10; [EXTRA] encoding pitfall  
**Suggested tools:** Python 3.11+; installed CNS library helpful

## Mission

A developer wrote `SHA256( SHA256(password).hexdigest().encode() )` but the incident response report only says **double SHA-256**. The exact method is in the developer quote. Search the candidate passwords and identify which one produces the given result. Submit the password. Important: `.hexdigest().encode()` is not the same as `.digest()` or `bytes.fromhex(...)`.

## Provided files

- `stored_hash.txt`
- `candidate_passwords.txt`

## How to submit

Find the requested **answer** (not the flag) and run at the top of the lab folder:

```powershell
python check.py H02 "YOUR_ANSWER"
```

If the answer contains JSON, spaces or PowerShell-special characters, save it to a UTF-8 text file and use:

```powershell
python check.py H02 --file answer.txt
```

The checker decrypts `reward.bin` and prints a `cns{...}` flag **only for the correct answer**. It does not tell you which attack to use. Read `HINTS.md` only if needed.
