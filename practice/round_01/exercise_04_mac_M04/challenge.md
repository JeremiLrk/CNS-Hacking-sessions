# M04 — Nested JSON discrepancy

**Category:** MAC/HMAC  
**Difficulty:** 5 / 5  
**Relevant slides:** Part 3 pp. 49–57 and 64–71; parser discrepancy [EXTRA]  
**Suggested tools:** Python 3.11+; installed CNS library helpful

## Mission

A service signs **canonical JSON** with HMAC. The authenticator uses Python-style JSON parsing (last duplicate object key wins), then sorts keys. The authorizer uses a buggy stream parser (first duplicate object key wins). You have a valid signature for a normal viewer request. Create a new **compact JSON body** that is still verified as viewer but is interpreted as admin **inside the nested `request` object**. Submit the raw compact JSON text (not its hash). The `action` must remain `read`, and `region` must remain `north`. You may reuse the supplied signature.

## Provided files

- `signed_request.json`
- `parser_behavior.txt`

## How to submit

Find the requested **answer** (not the flag) and run at the top of the lab folder:

```powershell
python check.py M04 "YOUR_ANSWER"
```

If the answer contains JSON, spaces or PowerShell-special characters, save it to a UTF-8 text file and use:

```powershell
python check.py M04 --file answer.txt
```

The checker decrypts `reward.bin` and prints a `cns{...}` flag **only for the correct answer**. It does not tell you which attack to use. Read `HINTS.md` only if needed.
