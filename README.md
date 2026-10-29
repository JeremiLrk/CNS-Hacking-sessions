# CNS Cryptography — Exam Toolkit

**Practical, beginner-friendly Python tools for the UAntwerpen Computer & Network Security hacking sessions.** This repository is organized so you can find a technique quickly, run it on Ubuntu, and understand *why* it works. It contains reusable tools, walkthroughs of **17 past challenges**, and **12 practice problems** arranged in three rounds.

> **Use only in the course lab or on systems you own or have permission to test.** These scripts demonstrate cryptographic implementation errors; they do not break properly implemented AES, SHA-256, or HMAC.

## Find what you need

| I need to... | Open |
|---|---|
| Recognize an attack from a challenge description | **[Attack playbook](docs/ATTACK_PLAYBOOK.md)** |
| Understand how to use Ubuntu, `nc`, `curl`, pipes or file formats | **[Ubuntu & terminal tutorial](docs/UBUNTU_TERMINAL.md)** |
| Learn Python byte operations, strings, encoding and the syntax used here | **[Python basics](docs/PYTHON_BASICS.md)** |
| Copy a small, reusable Python function | **[`tools/`](tools/)** |
| Run a ready-made attack template with my own inputs | **[`tools/recipes/`](tools/recipes/)** |
| Compare original and cleaned-up solutions to old CNS exercises | **[`past-exercises/`](past-exercises/)** |
| Solve a new challenge without reading the solution | **[`practice/`](practice/)** |

## Structure

```text
CNS-Cryptography-Exam-Toolkit/
├── README.md                     ← This orientation page
├── requirements.txt              ← Optional crypto dependencies
├── docs/
│   ├── ATTACK_PLAYBOOK.md        ← Symptoms → attack idea → exact code to try
│   ├── UBUNTU_TERMINAL.md        ← netcat, curl, tcp, HTTP, shell essentials
│   └── PYTHON_BASICS.md          ← Python explained in simple language
├── tools/
│   ├── basics/                   ← Hex/Base64, XOR, Caesar, Vigenère, file bytes
│   ├── stream/                   ← Reused keystream, Salsa20, ChaCha20, RC4, LCG
│   ├── block/                    ← AES, DES, ECB/CBC/CTR, padding, MITM
│   ├── hash/                     ← SHA family, length extension, HMAC, passwords
│   ├── web/                      ← JWT, JSON, RTSP Digest, HTTP
│   └── recipes/                  ← Runnable CLI examples (`python3 -m ...`)
├── past-exercises/
│   ├── README.md                 ← Index to your 17 already-solved challenges
│   └── 01_caesar/ ... 17_jwt/
│       ├── original.py          ← Your submitted approach + gentle comments
│       ├── solution.py          ← Cleaner/generalized approach
│       ├── README.md            ← What the vulnerability was and how to run it
│       └── data/                ← Challenge inputs, only where necessary
└── practice/
    ├── README.md                 ← Three-round exercise roadmap
    ├── check.py                  ← Locally check your answer and reveal `cns{...}`
    ├── round_01/                 ← Stream, block, hash, HMAC/MAC
    ├── round_02/                 ← Same four topics, harder variations
    └── round_03/                 ← Final four topics
        └── exercise_.../
            ├── challenge.md     ← Read this first
            ├── README.md        ← The exercise and the included files
            ├── [input files]     ← JSON, ciphertext, etc., kept together
            └── solution.py      ← OPEN ONLY AFTER TRYING IT YOURSELF
```

Some past exercises only have `solution.py`: no `original.py` was supplied for them, so no pretend original was created.

## Ubuntu: start without special software

Open **Terminal** (`Ctrl` + `Alt` + `T`) and enter:

```bash
# Clone the repository after publishing it, then enter its folder:
git clone https://github.com/JeremiLrk/CNS-Hacking-sessions.git
cd CNS-Hacking-sessions

# Check Python and built-in tools:
python3 --version
python3 -m tools.recipes.xor_reuse --help

# Run a standalone tool or an old solved exercise:
python3 tools/stream/nonce_reuse_solver.py
python3 past-exercises/13_better_hash/solution.py

# Practise, then check the answer locally:
python3 practice/check.py S08 'YOUR_ANSWER'
```

Most encoding, hashing, XOR and classical-cipher examples need **only Python 3**. For optional AES/DES/Salsa20 code on a machine where you can install packages:

```bash
sudo apt update
sudo apt install -y python3-venv python3-pip netcat-openbsd curl jq xxd
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

**If package installation is restricted during the exam:** many standalone tools still work; the [Ubuntu tutorial](docs/UBUNTU_TERMINAL.md) explains your options and which commands are already available.

## How to approach a new hacking-session question

1. **Read the prompt and find the clue.** Repeated nonce? Same-looking AES blocks? Truncated hash? Signed JSON? JWT header?
2. Open the **[Attack Playbook](docs/ATTACK_PLAYBOOK.md)** and search (`Ctrl+F`) for that clue.
3. Pick a matching helper in `tools/` or a runnable file from `tools/recipes/`.
4. Change the clearly marked inputs, and inspect the **bytes** as well as text.
5. If stuck, compare the corresponding file in `past-exercises/`. For new questions, avoid `solution.py` until you have attempted the problem.

## The three practice rounds

| Round | Stream cipher | Block cipher | Hashing | MAC / HMAC / authentication |
|---|---|---|---|---|
| **1** | S08 — nonce reuse | B03 — ECB splicing | H02 — double SHA | M04 — signed JSON |
| **2** | S06 — weak PRNG | B04 — CBC IV | H06 — length extension | M03 — JWT algorithm |
| **3** | S05 — ChaCha counter | B10 — double AES | H07 — collision | M02 — RTSP Digest |

Go to [practice/README.md](practice/README.md) for the actual directories and checker commands. Each challenge keeps its inputs in its own folder.

## A note on the solutions and source material

- The **17 original challenges** were solved by the student; some rely on live course services that cannot be reproduced offline. `original.py` preserves the supplied approach; `solution.py` is a readable version, not a claim that the original was incorrect.
- The **12 newer practice exercises** are original training problems and include a self-checker. Their `solution.py` files are intentionally easy to find, but contain spoilers.
- Don't publish private credentials or course files that aren't yours to redistribute. Check any third-party capture or wordlist's licensing before distributing this repo.
- This repository is a study aid, **not** official UAntwerpen coursework or course answers.