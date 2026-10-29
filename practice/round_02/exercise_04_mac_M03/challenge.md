# M03 — JWT algorithm switch

**Category:** MAC/HMAC  
**Difficulty:** 4 / 5  
**Relevant slides:** Part 3 pp. 64–71; JWT [EXTRA]  
**Suggested tools:** Python 3.11+; installed CNS library helpful

## Mission

A demo session token is signed with HS256, and it belongs to a viewer. A vulnerable training validator lets the JWT header choose the verification algorithm and mistakenly accepts unsigned tokens. Forge a JWT for the SAME `sub=guest-007` but `role=admin`, using the insecure `alg=none` behavior. This time, the third JWT segment must be **empty** (still keep the final dot). Submit the exact forged token string. Do not try to crack its HMAC secret.

## Provided files

- `guest_jwt.txt`
- `claims.json`
- `validator_note.txt`

## How to submit

Find the requested **answer** (not the flag) and run at the top of the lab folder:

```powershell
python check.py M03 "YOUR_ANSWER"
```

If the answer contains JSON, spaces or PowerShell-special characters, save it to a UTF-8 text file and use:

```powershell
python check.py M03 --file answer.txt
```

The checker decrypts `reward.bin` and prints a `cns{...}` flag **only for the correct answer**. It does not tell you which attack to use. Read `HINTS.md` only if needed.
