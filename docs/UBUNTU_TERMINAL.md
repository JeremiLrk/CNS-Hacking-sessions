# Ubuntu terminal field guide — Python, netcat, curl, bytes and JSON

A **hands-on exam reference**, written for someone who knows Python but gets stuck on Linux commands. The examples below are for **your authorized CNS lab**. You can replace host/port with an exam-provided target.

## 0. What is a terminal, what is the `$` sign?

In examples, `$` means the shell is waiting for a command. **Do NOT type the `$` itself**.

```bash
pwd                       # Where am I right now?
ls -lah                   # Show files (including hidden files)
cd /home/student/CNS_Crypto_Exam_Repo
ls
cd ..                     # Move to parent folder
clear                     # Clean the terminal display
```

`Ctrl+C` stops the running command. `Ctrl+D` sends end-of-file to a program reading from stdin. `Ctrl+Shift+C` copies in many Linux terminals; `Ctrl+Shift+V` pastes. `Ctrl+Z` merely suspends a running program (it doesn't always terminate it).

## 1. Install tools on Ubuntu

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip netcat-openbsd curl jq xxd git
```

Meaning: `sudo` uses administrator privileges; `apt` installs Ubuntu packages; `-y` answers yes automatically.

A university lab computer may **not allow `sudo`**. If so, check if tools already exist:

```bash
python3 --version
which python3
which nc
which curl
which jq
python3 -c 'import hashlib; print(hashlib.sha256(b"abc").hexdigest())'
```

Python's `hashlib`, `hmac`, `json`, `base64`, `socket`, `urllib` and `binascii` are built in. Most tools here need nothing else.

### Installing crypto libraries without breaking Ubuntu Python

```bash
cd CNS_Crypto_Exam_Repo
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -c 'from Crypto.Cipher import AES; print("AES library works")'
```

`(.venv)` in your prompt indicates that this virtual environment is active. To exit it:

```bash
deactivate
```

If Python says `externally-managed-environment`, **use a venv**; do not force pip into Ubuntu's system Python. If you can't download packages during the exam, install/test before the exam or stick to the standard-library scripts.

## 2. netcat (`nc`) — talk to raw TCP services

**Think of netcat as a simple window into a TCP connection.** It writes what you type to a server and displays what it sends back. It does NOT automatically do HTTPS, parse JSON, or decode encryption.

### Test whether a port is reachable

```bash
nc -vz -w 4 cns-test.idlab.uantwerpen.be 50001
```

- `-v`: verbose; show connection status.
- `-z`: only check whether the port accepts a connection, don't send data.
- `-w 4`: set a 4-second timeout. (Flags vary slightly by netcat variant; Ubuntu's `netcat-openbsd` supports them.)

`Connection refused` means the host is reachable but no service accepts that port (or an explicit rejection happened). `timed out` means nothing answered; possible VPN, firewall, routing or offline server. **A failed ping does not prove TCP is blocked**.

### Connect and type manually

```bash
nc cns-test.idlab.uantwerpen.be 50001
```

Now the **same terminal** is connected. If the program says `Submit the transaction (hex):`, paste a hex string and press **Enter**. `Ctrl+C` exits netcat.

To turn text into hex before submitting:

```bash
printf '%s' 'hello' | xxd -p -c 1000
```

`printf '%s'` is important: it does **not** add a newline, unlike many uses of `echo`. An extra `\n` byte changes hashes and signatures.

### Send lines from a file

```bash
printf 'first line\nsecond line\n' | nc -w 5 cns-test.idlab.uantwerpen.be 50003
```

If a server expects **two JSON records, each on one line**:

```bash
printf '%s\n%s\n' \
  '{"reference":"PAY-1","from_account":"SIM-A","to_account":"SIM-B","amount":10,"currency":"EUR","timestamp":"2026-10-29T09:00:00+00:00"}' \
  '{"reference":"PAY-2","from_account":"SIM-A","to_account":"SIM-B","amount":10,"currency":"EUR","timestamp":"2026-10-29T09:00:00+00:00"}' \
  | nc -w 5 cns-test.idlab.uantwerpen.be 50003
```

Those are demonstration JSON objects, not guaranteed to be currently accepted. Change the timestamp to satisfy the challenge's rules.

### Save server replies so you can inspect them

```bash
printf 'HELLO\n' | nc -w 5 example.org 12345 | tee response.txt
```

`tee` displays output AND saves it to a file. Replace `example.org:12345` with the actual target; no claim that this example service exists.

### Convert a saved server hex response to bytes

```bash
xxd -r -p ciphertext.hex > ciphertext.bin
xxd -g 1 ciphertext.bin | head
```

`xxd -r -p` takes hex ASCII → actual bytes; `xxd -p` does the reverse.

### If nc gets stuck

- Is the server waiting for a newline? Press Enter.
- Does it require two separate lines? Send both.
- Does it wait until end-of-input? Use `printf ... | nc -N host port` (OpenBSD netcat `-N` closes after stdin EOF).
- Does it need VPN? Connect to the university VPN first.
- `Ctrl+C` disconnects; don't kill your entire shell.

## 3. `curl` — HTTP requests, not raw TCP

`curl` makes web requests (GET, POST, etc.). **Never use netcat for an ordinary API unless the task explicitly asks for raw bytes**.

### GET a web endpoint

```bash
curl -i http://cns-test.idlab.uantwerpen.be:50007/challenge
```

`-i` includes HTTP response headers: status codes (`200`, `401`, `403`), `Content-Type`, etc.

### A quiet GET that still shows errors

```bash
curl -sS http://cns-test.idlab.uantwerpen.be:50009/login
```

`-s` silences progress; `-S` displays error messages even in silent mode.

### Pretty-print JSON response

```bash
curl -sS http://cns-test.idlab.uantwerpen.be:50007/challenge | python3 -m json.tool
```

Or with `jq`:

```bash
curl -sS http://cns-test.idlab.uantwerpen.be:50007/challenge | jq .
```

### POST JSON with a custom HMAC header

Create the RAW request body as a file with a quoted here-document. This preserves duplicate JSON keys and avoids Bash interpreting `$`, quotes, etc.

```bash
cat > body.json <<'JSON'
{"action":"view","role":"admin","role":"user"}
JSON
```

Send the body with the original signature:

```bash
curl -i -sS -X POST \
  'http://cns-test.idlab.uantwerpen.be:50007/vault' \
  -H 'Content-Type: application/json' \
  -H 'X-Signature: PASTE_THE_LAB_SIGNATURE_HERE' \
  --data-binary @body.json
```

**Why `--data-binary @body.json`?** It sends the bytes from the file. This matters in tasks where signatures are checked over exact data. `--data` can process input differently. If the application canonicalizes parsed JSON before HMAC verification, it may ignore harmless whitespace, but **don't assume** that.

### Send JWT as Bearer token

```bash
TOKEN='PASTE_THE_TOKEN_HERE'
curl -i -sS \
  -H "Authorization: Bearer $TOKEN" \
  'http://cns-test.idlab.uantwerpen.be:50009/admin'
```

The exact header name/cookie format depends on the challenge. If the server expects `Cookie: token=...`, a Bearer header will not work. Read the challenge instructions and request examples.

### Change the method and show diagnostics

```bash
curl -v -X POST -H 'Content-Type: application/json' \
  --data-binary @body.json 'http://example.org/api'
```

`-v` (verbose) shows request/response details including headers. This may reveal secrets in your terminal output; do not upload verbose logs containing authorization tokens to public GitHub.

### Save response body and status separately

```bash
curl -sS -o response.json -w 'HTTP status: %{http_code}\n' \
  'http://example.org/api'
cat response.json
```

### Common HTTP errors

| Code | Usually means | What to check |
|---|---|---|
| 200 | Request accepted | Look at body for flag |
| 400 | Invalid format | JSON syntax, fields, encoding, method |
| 401 | Not authenticated | Token, HMAC, credentials, header |
| 403 | Authenticated but forbidden | Role/permissions/authorization |
| 404 | Wrong path | Exact endpoint and slash |
| 405 | Wrong method | GET vs POST |
| 500 | Server bug | Avoid interpreting as guaranteed exploit success |

## 4. JSON tricks: do NOT accidentally destroy duplicates

`json.dumps({'role':'admin','role':'user'})` is NOT possible: Python dictionaries cannot contain two separate `role` entries. Build the **raw string** instead.

```bash
printf '%s' '{"role":"admin","role":"user"}' > body.json
cat body.json
```

To inspect how Python handles duplicate keys:

```bash
python3 - <<'PY'
import json
raw='{"role":"admin","role":"user"}'
print(json.loads(raw))  # Python keeps the LAST role
PY
```

For canonical JSON, Secure Bank 2 used sorted keys and compact formatting:

```bash
python3 -c 'import json,hashlib; b=json.dumps({"z":2,"a":1},sort_keys=True,separators=(",",":"),ensure_ascii=True).encode(); print(b,hashlib.sha256(b).hexdigest())'
```

Different spaces, Unicode escaping, key order and number representation can change the digest if the service signs raw bytes. Match its actual `canonicalize` function.

## 5. Byte tricks that save minutes in the exam

```bash
# Hex text to actual bytes
python3 -c 'print(bytes.fromhex("636e73"))'

# Bytes to hex
python3 -c 'print(b"cns".hex())'

# Base64 decode
printf '%s' 'Y25z' | base64 -d

# Base64 encode (no accidental newline)
printf '%s' 'cns' | base64

# File signature
file encrypted.bmp
xxd -l 64 -g 1 encrypted.bmp

# SHA-256 of exactly the bytes "hello" (no newline)
printf '%s' 'hello' | sha256sum

# SHA-256 of real bytes decoded from hex "4142" (= AB)
printf '4142' | xxd -r -p | sha256sum
```

**Important:** `sha256sum` shows the hash of raw stdin bytes, not the hash of printed hex string unless you choose to send that string.

## 6. Put the repo on GitHub and download it on Ubuntu

Use GitHub's **New Repository** UI to create an empty public repository. Then from inside this extracted folder:

```bash
git init
git branch -M main
git add .
git commit -m 'Organized CNS cryptography toolkit'
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

If GitHub rejects password authentication, use a GitHub token or the GitHub CLI. A normal account password isn't accepted as Git HTTPS authentication.

To clone on the exam PC:

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO
```

If network access is restricted during the exam, download this repo ZIP beforehand. `git clone` requires internet access.

### GitHub CLI shortcut if `gh` is installed

```bash
gh auth login
gh repo create cns-crypto-exam-toolkit --public --source . --remote origin --push
```

Before publication, check distribution rights for university-supplied exercise files, wordlists and captures. Do not add credentials, API keys or tokens.

## 7. Troubleshooting checklist

1. Which protocol? `nc` for raw TCP, `curl` for HTTP.
2. Which encoding? Text, hex ASCII, Base64, binary or JSON?
3. Which bytes are encrypted and which form nonce, IV, tag or header?
4. Does server expect one line, two JSON lines, HTTP body or header?
5. Is it a connection, format or crypto issue?
6. When signatures fail, did you accidentally append a newline?
7. Before debugging the cipher, inspect exact input/output bytes (`xxd -g 1`).
