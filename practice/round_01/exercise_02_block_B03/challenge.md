# B03 — Cut-and-paste access badges

**Category:** Block  
**Difficulty:** 4 / 5  
**Relevant slides:** Part 2 pp. 101–102  
**Suggested tools:** Python 3.11+; installed CNS library helpful

## Mission

A broken controller uses AES-ECB and stores three independent 16-byte blocks. You captured ciphertext for a 3-block GUEST request. Separately, an ADMIN role block was legitimately encrypted by the same key. Build a 3-block ciphertext that requests ADMIN while keeping **CMD** and **ZONE** intact. You may splice encrypted blocks, but cannot encrypt arbitrary plaintext. Submit the combined ciphertext as lowercase hex.

## Provided files

- `original_request.hex`
- `admin_role_block.hex`
- `format.txt`

## How to submit

Find the requested **answer** (not the flag) and run at the top of the lab folder:

```powershell
python check.py B03 "YOUR_ANSWER"
```

If the answer contains JSON, spaces or PowerShell-special characters, save it to a UTF-8 text file and use:

```powershell
python check.py B03 --file answer.txt
```

The checker decrypts `reward.bin` and prints a `cns{...}` flag **only for the correct answer**. It does not tell you which attack to use. Read `HINTS.md` only if needed.
