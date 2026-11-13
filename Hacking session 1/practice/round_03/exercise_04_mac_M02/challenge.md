# M02 — RTSP Digest with qop=auth

**Category:** MAC/HMAC  
**Difficulty:** 4 / 5  
**Relevant slides:** Part 3 pp. 85–92; Digest Auth [EXTRA]  
**Suggested tools:** Python 3.11+; installed CNS library helpful

## Mission

A network capture contains an RTSP Digest authentication exchange. This version includes **qop=auth, nc and cnonce**, unlike the simple 3-term formula you used before. The username, realm, method, URI, nonce and target response are all captured. Crack the password from the attached wordlist. Submit the password. Use `HA1=MD5(user:realm:password)`, `HA2=MD5(method:uri)` and `response=MD5(HA1:nonce:nc:cnonce:qop:HA2)`.

## Provided files

- `rtsp_capture.txt`
- `passwords.txt`

## How to submit

Find the requested **answer** (not the flag) and run at the top of the lab folder:

```powershell
python check.py M02 "YOUR_ANSWER"
```

If the answer contains JSON, spaces or PowerShell-special characters, save it to a UTF-8 text file and use:

```powershell
python check.py M02 --file answer.txt
```

The checker decrypts `reward.bin` and prints a `cns{...}` flag **only for the correct answer**. It does not tell you which attack to use. Read `HINTS.md` only if needed.
