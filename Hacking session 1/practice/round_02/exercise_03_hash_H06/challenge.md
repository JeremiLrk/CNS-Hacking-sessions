# H06 — Length extension at the archive gate

**Category:** Hashing  
**Difficulty:** 5 / 5  
**Relevant slides:** Part 3 pp. 32–35  
**Suggested tools:** Your CNS toolkit SHA256 length-extension helper

## Mission

An old API authenticates requests with `SHA256(secret || message)`, **not HMAC**. The secret key length is an unknown integer between 9 and 18 bytes. You know one valid message and its hash. Append the raw byte sequence `&role=supervisor` using a SHA-256 length-extension attack. Find a valid `(forged_message, forged_digest)` pair. Submit exactly `forged_message_hex:forged_digest_hex` (lowercase, no spaces). The forged message must contain SHA-256 *glue padding bytes*, not simply the old readable text plus the new field.

## Provided files

- `signed_request.json`

## How to submit

Find the requested **answer** (not the flag) and run at the top of the lab folder:

```powershell
python check.py H06 "YOUR_ANSWER"
```

If the answer contains JSON, spaces or PowerShell-special characters, save it to a UTF-8 text file and use:

```powershell
python check.py H06 --file answer.txt
```

The checker decrypts `reward.bin` and prints a `cns{...}` flag **only for the correct answer**. It does not tell you which attack to use. Read `HINTS.md` only if needed.
