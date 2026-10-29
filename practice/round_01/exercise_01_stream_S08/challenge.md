# S08 — The nonce collision hunt

**Category:** Stream  
**Difficulty:** 4 / 5  
**Relevant slides:** Part 2 pp. 46–58  
**Suggested tools:** Python 3.11+; installed CNS library helpful

## Mission

Seven Salsa20 packets were captured. Six contain unstructured private bytes, but one contains a known public status message. Find which packets reused the *same nonce*, then use that **matching pair only** to recover `RELAY CONTROL KEY`. Other packets are red herrings. Submit the recovered key value.

## Provided files

- `packets.json`
- `public_message.bin`

## How to submit

Find the requested **answer** (not the flag) and run at the top of the lab folder:

```powershell
python check.py S08 "YOUR_ANSWER"
```

If the answer contains JSON, spaces or PowerShell-special characters, save it to a UTF-8 text file and use:

```powershell
python check.py S08 --file answer.txt
```

The checker decrypts `reward.bin` and prints a `cns{...}` flag **only for the correct answer**. It does not tell you which attack to use. Read `HINTS.md` only if needed.
