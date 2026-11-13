# CNS ATTACK PLAYBOOK — vulnerabilities, tricks and executable recipes
## When I see X, which trick should I try? — beginner-friendly exam reference

**Read this file when an exercise gives you an unfamiliar encryption algorithm, a hash, a MAC, a JWT, JSON, or a network capture.** This file is a practical attack map. It does **not** mean every algorithm has a break. Strong algorithms, correctly implemented, should resist these attacks.

### What the labels mean

- **[COURSE CONCEPT]**: a mathematical/cryptographic concept covered by the course topics (classical, stream, block, hashing, MACs).
- **[CTF / EXTRA]**: an implementation mistake or attack technique useful in the hacking exercises; not necessarily explained in the lecture slides.
- **[PAST CNS]**: a pattern from the earlier CNS exercises you supplied.
- **Needs** = conditions that **must** hold before the trick works. Without them, do not assume success.

> **RULE #1:** Do not start by randomly decrypting. First identify the algorithm, which data is *plaintext*, which data is *ciphertext*, what is secret, and what is public. Most CTF bugs come from how the algorithm is **used**, not the algorithm itself.
>
> **RULE #2:** `hex`, Base64, and Base64url are **encodings**, not encryption. `SHA-256` is **hashing**, not encryption. `HMAC` authenticates data; it does **not** encrypt the message.

---

# 0. Fast decision tree — try this in the first minute

| What you see | First idea | Where in toolkit |
|---|---|---|
| `616263` or another long hex value | Convert hex to bytes. Check if it contains readable text, a hash, or binary ciphertext. | `tools/basics/encoding_for_beginners.py` |
| `eyJ...`.`eyJ...`.`...` | Likely JWT: decode header AND payload; inspect `alg` and `role`. | `tools/web/jwt_for_beginners.py` |
| Two ciphertexts with the same nonce / IV | Look for **reused keystream** (CTR/OFB/stream ciphers), or mode-specific issues (CBC is different!). | `tools/stream/nonce_reuse_solver.py`, `tools/block/aes_modes.py` |
| Plaintext + its ciphertext, and another ciphertext | Known-plaintext attack, **if the same keystream was used**. | `tools/stream/nonce_reuse_solver.py` |
| Secret-prefix SHA-256/MD5/SHA-1 hash | Consider **length extension** if the MAC is `hash(secret || message)` rather than HMAC. | `tools/hash/sha256_length_extension.py` |
| Hash output strangely short | Possible **truncated-hash collision**. About `2^(bits/2)` attempts for a collision. | `tools/hash/hash_functions.py` |
| JSON with valid HMAC but server refuses admin | Examine **what bytes were signed** versus **what JSON is parsed**. Try duplicate keys in an authorized lab. | `tools/web/json_parser_tricks.py` |
| Guest JWT and admin endpoint | Examine algorithm validation, claims, and whether the server enforces signature verification. | `tools/web/jwt_for_beginners.py` |
| DES key has known fixed prefix | Search only the unknown part of the key, not all 56 bits. | `tools/block/des_small_key_solver.py` |
| Double encryption with two small keys | Consider **meet-in-the-middle**, not trying every key *pair*. | `tools/block/double_aes_mitm.py` |
| AES-ECB ciphertext split into 16-byte blocks | Check repeating blocks and possibility of **block swapping**. | `tools/block/aes_modes.py` |
| AES-CBC with changeable IV | Think `new_IV = old_IV XOR old_P1 XOR desired_P1`. | `tools/block/cbc_iv_bit_flipping.py` |
| Network capture with `Authorization: Digest` | Record username, realm, nonce, URI, method and response; test candidate passwords offline. | `tools/web/rtsp_digest_solver.py` |
| Given an algorithm's actual Python implementation | Read the code! Look for tiny keyspaces, home-made hashes, integer overflows, unsafe nonce generation, bad comparisons. | `past-exercises/` |

**Critical distinction:** two equal IVs in CBC do **not** give the simple `P2 = P1 XOR C1 XOR C2` formula. That formula needs **identical XOR keystreams** (stream ciphers, OTP reuse, AES-CTR with same counter start, etc.).

---

# 1. CLASSICAL CIPHERS — what can go wrong?

## 1.1 Caesar / shift cipher — [COURSE CONCEPT] [PAST CNS]

**Recognize it:** alphabetic ciphertext; letters shifted by a fixed number; same structure/spacing.

**Try:** all 26 shifts. You do not need a dictionary or a huge computer. Check if known words or `cns{` appear. For simple uppercase/lowercase text, leave `{`, `}`, `-`, spaces unchanged.

**Why:** the secret key is just one of 26 possibilities.

**Toolkit:** `tools/basics/classical_ciphers.py`, `past-exercises/01_caesar.py`.

## 1.2 Monoalphabetic substitution / Switcheroo — [COURSE CONCEPT] [PAST CNS]

**Recognize it:** two 26-letter alphabets are given (plain alphabet and scrambled alphabet), or a long English-looking cryptogram with spaces and letter repetitions.

**Try:** reverse the mapping when decrypting! Example: plaintext `A` maps to ciphertext `Q`, so ciphertext `Q` must map back to `A`. When no alphabet is supplied, use frequency analysis, one-letter words, word patterns, and a dictionary.

**Gotcha:** letter-frequency ranking **alone** usually gives a rough guess, not the full answer. Short ciphertexts are especially unreliable.

**Toolkit:** `tools/basics/classical_ciphers.py`, `04_count_the_letters.py`, `02_switcheroo.py`.

## 1.3 Vigenère — [COURSE CONCEPT] [PAST CNS]

**Recognize it:** a repeated password/keyword, multiple different shifts, ciphertext still contains only letters, sometimes a clue like a food or place name.

**Try:** clue-based keyword first. If the key is unknown, estimate key length (repeated groups / index of coincidence), then analyse each key position as a Caesar cipher.

**Important implementation detail:** some variants advance the key on letters **only**; others advance on **all characters** including punctuation. You must match the challenge's specification. The toolkit's ordinary Vigenère helper advances on letters only.

**Toolkit:** `tools/basics/classical_ciphers.py`, `03_french_cipher_vigenere.py`.

## 1.4 Rotor / toy Enigma — [COURSE CONCEPT] [PAST CNS]

**Recognize it:** several permuted alphabet strings that rotate after each input letter.

**Try:** carefully reproduce *when* stepping happens (BEFORE or AFTER processing); reverse the path through the rotors for decryption; rotate the next rotor only on a full turnover.

**Gotchas:** symbols do not necessarily step; rotor 2 and 3 positions depend on the number of **processed letters**, not raw string length; invert each rotor mapping in reverse order rather than applying forward lookup again.

**Toolkit:** `past-exercises/06_my_first_enigma.py`.

## 1.5 Transposition / column rearrangement — [CTF / EXTRA]

**Recognize it:** nearly normal frequencies (same letters as plaintext) but the words are scrambled. The alphabet was not changed, only **positions**.

**Try:** test plausible column widths and reconstruct columns in the correct read-out order.

## 1.6 Affine cipher — [CTF / EXTRA]

**Recognize it:** rule `E(x) = (a*x + b) mod 26` or a substitution with two small numeric parameters.

**Try:** enumerate `b` from 0–25 and invertible `a` values with `gcd(a,26)=1`. The inverse exists **only when** `a` and 26 are coprime.

---

# 2. STREAM CIPHERS, OTP, RC4, SALSA20, CHACHA20, AES-CTR

## 2.1 One-Time Pad (OTP) — [COURSE CONCEPT]

**Correct OTP:** truly random secret keystream, as long as the message, **used once**. You cannot deduce plaintext from ciphertext alone.

**Vulnerability:** using the same pad twice. Then `C1 XOR C2 = P1 XOR P2`. A known plaintext can reveal the matching portion of the other plaintext.

**Do not attempt:** brute forcing a correctly used true OTP. There is no unique answer from ciphertext alone.

## 2.2 Same key + same nonce + same counter start — [COURSE CONCEPT] [PAST CNS]

**Algorithms to check:** Salsa20, ChaCha20, AES-CTR, OFB, reused OTP, and RC4 restarted with the same secret key/initial state.

**Recognize it:** duplicate `nonce_hex`, duplicate IV in a stream-like mode, or two messages built from identical stream cipher settings.

**Try:** find a plaintext you know and its matching ciphertext, then:

```python
# Every value must be raw bytes and aligned at the same position.
keystream = bytes(a ^ b for a, b in zip(known_plaintext, known_ciphertext))
recovered  = bytes(a ^ b for a, b in zip(secret_ciphertext, keystream))
print(recovered)
```

**Formula:** `S = P1 XOR C1`; `P2 = C2 XOR S`. You recover a *keystream*, NOT the secret Salsa20/ChaCha20/AES key.

**Gotchas:** same nonce is useful only when the **key also matches**; messages may start at different counter values; a packet may contain `nonce || ciphertext` — remove the nonce before XOR; only the known part of the plaintext can be recovered.

**Toolkit:** `tools/stream/nonce_reuse_solver.py`; `10_noncense_double_xor.py`.

## 2.3 Ciphertext bit flipping — [CTF / EXTRA] [PAST CNS]

**Recognize it:** ciphertext is not authenticated, you know bytes of the ORIGINAL plaintext, and you want to replace an amount, role, account number, etc.

**Try:** `new_C = old_C XOR old_P XOR desired_P` **at the correct byte position**.

**Needs:** the original plaintext bytes at that offset; same number of bytes in old/new; stream-like XOR encryption **without effective authentication**. AES-GCM and ChaCha20-Poly1305 should reject a changed ciphertext if the tag is correctly checked.

**Gotchas:** JSON separators, quotation marks, spaces, encoding and nonce prefix change offsets. Always count bytes, not just visible characters.

**Toolkit:** `tools/stream/nonce_reuse_solver.py`; `08_secure_bank_salsa20.py`.

## 2.4 Ciphertext-only attacks on reused streams — [CTF / EXTRA]

**Recognize it:** two ciphertexts with a repeated nonce, but no complete known plaintext.

**Try:** `C1 XOR C2`; guess likely words/headers in one plaintext, XOR those guesses against the corresponding segment, look for sensible text in the other (`crib dragging`). Repeated JSON field names, `HTTP/1.1`, `cns{`, and file headers are potential cribs **only if they fit the actual format**.

**Important:** a possible English-looking result is a guess until you validate more bytes.

## 2.5 Weak PRNG / LCG used as keystream — [COURSE CONCEPT + CTF / EXTRA] [PAST CNS]

**Recognize it:** custom code such as `state = (A*state+C) % M` and keystream bytes derived from bits of the state.

**Try:** known plaintext reveals output bytes; recover a consistent internal state/seed, then reproduce the keystream and decrypt. The implementation matters: do not blindly reuse constants from a different exercise.

**Gotcha:** different seeds can produce the same observed bytes. Verify by reproducing *all* known bytes and decrypting the secret, not merely accepting the first candidate.

**Toolkit:** `tools/stream/weak_lcg_solver.py`; `07_replanting_weak_prng.py`.

## 2.6 RC4 — [COURSE CONCEPT]

**Recognize it:** 256-byte state array, key-scheduling algorithm (KSA), swaps, pseudo-random byte generation (PRGA).

**Try:** understand the exact KSA/PRGA and XOR output. RC4 with the **same key and same initial state** starts with the same keystream (bad). Known statistical biases also exist, but exploiting them usually needs many samples; one ciphertext is not enough for a magical instant break.

**Toolkit:** `tools/stream/rc4_for_learning.py`.

## 2.7 Salsa20 / ChaCha20 internals — [COURSE CONCEPT]

**Recognize it:** ARX operations — integer **A**ddition mod `2^32`, bit **R**otation, **X**OR; quarter-rounds, counter, nonce.

**Try:** track little-endian words, 32-bit wraparound (`& 0xffffffff`), exact rotation counts, correct nonce/counter layout. If asked to decrypt using a known key, use the library instead of manually implementing the whole cipher.

**Bug patterns:** repeated nonce/counter; wrong counter offsets; home-made counter format; missing MAC. Do **not** confuse algorithm correctness with the surrounding protocol's security.

**Toolkit:** `tools/stream/modern_stream_ciphers.py`.

---

# 3. BLOCK CIPHERS — DES, 3DES, AES, ECB, CBC, CFB, OFB, CTR, XTS

## 3.1 DES fixed key prefix / small search space — [COURSE CONCEPT] [PAST CNS]

**Recognize it:** DES key is 8 bytes but 6 or 7 bytes are hard-coded, so only 1–2 bytes are unknown.

**Try:** brute force only the unknown portion; decrypt each candidate; validate a known header, format, and padding.

**Important:** DES has an effective key size of 56 bits because of parity. That does **not** mean every DES challenge should search all `2^56` keys! The *challenge's key generator* may reduce the work dramatically.

**Toolkit:** `tools/block/des_small_key_solver.py`; `09_key_standardisation_DES.py`.

## 3.2 3DES / EDE — [COURSE CONCEPT]

**Recognize it:** encrypt with K1, decrypt with K2, encrypt with K3; multiple 8-byte DES keys.

**Try:** identify how many key bytes are unknown; if only 1 byte is missing, brute-force 256 candidates. Match CBC/ECB, IV, and key parity according to library requirements.

**Gotcha:** 3DES is not the same thing as AES, and the three operations matter. A wrong IV can corrupt the first plaintext block while others might look okay.

## 3.3 Double encryption and meet-in-the-middle — [COURSE CONCEPT + CTF / EXTRA] [PAST CNS]

**Recognize it:** `C = E_K2(E_K1(P))` with two **small** independent keys.

**Try:** compute `E_K1(P)` for all possible K1 and save a lookup table. For every K2 compute `D_K2(C)` and look for a match. Confirm candidates using a **second independent known plaintext/ciphertext block**.

**Why:** changes a naive search of about `2^(2k)` key pairs into about `2^k` stored results plus `2^k` checks (memory is needed).

**CRITICAL:** if P is a BMP pixel block, do not *assume* it is `00 ff 00 ...` just because the file is a bitmap. The actual known plaintext block and **correct BMP pixel offset** must be justified by the file format.

**Toolkit:** `tools/block/double_aes_mitm.py`; `11_aes_2_meet_in_the_middle.py`.

## 3.4 AES-ECB: repeating blocks — [COURSE CONCEPT]

**Recognize it:** ciphertext length divisible by 16, identical 16-byte ciphertext blocks, repeated patterns in an encrypted image.

**Try:** split into 16-byte blocks and count duplicates. ECB encryption of identical plaintext blocks under the same key gives identical ciphertext blocks.

**Gotcha:** no repeated blocks does **not** prove ECB was not used.

## 3.5 AES-ECB: cut-and-paste / splicing — [CTF / EXTRA]

**Recognize it:** independently meaningful 16-byte fields (`CMD`, `ROLE`, `ZONE`) encrypted under the **same ECB key**, and you have a valid ciphertext block containing a useful role/value.

**Try:** move complete *encrypted 16-byte blocks*, not individual random bytes. Under ECB, each block decrypts separately.

**Needs:** compatible layout, same key, no signature/MAC on the full message. This does not work the same way under CBC or properly authenticated encryption.

**Toolkit:** `tools/block/aes_modes.py` for ECB basics; practise in exercise B03.

## 3.6 AES-CBC: change the IV to change plaintext block 1 — [COURSE CONCEPT + CTF / EXTRA]

CBC decryption for the **first** block:

`P1 = D_K(C1) XOR IV`

If you know P1 and want a same-length replacement P1_new:

`IV_new = IV_old XOR P1_old XOR P1_new`

**Needs:** IV editable or not authenticated. Ciphertext blocks stay unchanged. Only plaintext block 1 is targeted.

**Toolkit:** `tools/block/cbc_iv_bit_flipping.py`; practise in B04.

## 3.7 AES-CBC: edit previous ciphertext block — [CTF / EXTRA]

For a later block: `P_i = D_K(C_i) XOR C_(i-1)`.

So editing **C_(i-1)** changes **P_i** predictably, but also **scrambles P_(i-1)**. The attack only helps if that collateral damage is acceptable and there is no integrity protection.

**Needs:** known original bytes of target plaintext block and same-length desired bytes.

**Toolkit:** `tools/block/cbc_iv_bit_flipping.py`; practise in B05.

## 3.8 AES-CBC: padding oracle — [CTF / EXTRA]

**Recognize it:** server reveals **different behaviour** for incorrect PKCS#7 padding versus correct padding (distinct errors, timings or status codes).

**Try conceptually:** modify a previous block/IV and use the valid/invalid padding response to infer plaintext bytes. This requires repeated interaction with the vulnerable oracle; having CBC ciphertext alone is not enough.

**Gotcha:** different errors are evidence, not proof. AEAD or properly verified encrypt-then-MAC should prevent this attack.

## 3.9 PKCS#7 padding — [COURSE CONCEPT]

For block size 16, if the message is 14 bytes long, append `02 02`. If the plaintext is exactly 16 bytes, add a **whole new 16-byte padding block** (`10` repeated 16 times).

**Try:** remove padding *after* successful decryption and validation. Invalid padding often means wrong key, wrong mode, wrong IV/counter, corruption — not necessarily a padding-oracle challenge.

**Toolkit:** `tools/block/aes_modes.py`.

## 3.10 AES-CTR — [COURSE CONCEPT]

**Recognize it:** a block cipher encrypts `nonce || counter` to produce a keystream, which is XORed with message bytes.

**Try:** treat it like a stream cipher for **keystream reuse** and **bit flipping**, but only when key, nonce and counter positions align.

**Gotcha:** counter endianness (big vs little), counter width, nonce length and starting value vary by implementation.

**Toolkit:** `tools/block/aes_modes.py`, `tools/stream/nonce_reuse_solver.py`.

## 3.11 AES-OFB — [COURSE CONCEPT]

**Recognize it:** the output of AES repeatedly feeds back to create a stream, then XOR with plaintext.

**Try:** repeated key + IV produces repeated keystream; known plaintext can recover matching secret plaintext bytes.

**Gotcha:** changing the ciphertext usually changes the corresponding plaintext bytes without spreading damage, **unless** integrity protection detects it.

## 3.12 AES-CFB — [COURSE CONCEPT]

**Recognize it:** ciphertext feedback and a configurable segment size (often CFB-8 or CFB-128).

**Try:** check `segment_size`, IV, and alignment. Same key + IV can leak a shared initial keystream segment; changing ciphertext affects later plaintext for a limited distance, unlike CTR/OFB's simple independent byte effects.

**Gotcha:** **do not** automatically use the plain double-XOR rule over entire ciphertexts in CFB; feedback changes the generated stream once ciphertext diverges.

## 3.13 AES-XTS — [COURSE CONCEPT]

**Recognize it:** encrypting disk sectors; tweak depends on sector/block position; two AES keys.

**Try:** determine sector number, tweak format, AES key halves, block position and ciphertext-stealing rules. XTS is for confidentiality of stored sectors, **not** message authentication.

**Gotcha:** cannot usually decrypt one sector with a tweak from a different sector.

## 3.14 AES-GCM / AES-CCM — [COURSE CONCEPT]

**Recognize it:** ciphertext plus **nonce + authentication tag**, perhaps associated data (AAD).

**Try on a legitimate decryption task:** use exactly the original key, nonce, ciphertext, AAD and tag. If any changes, verification should fail.

**Vulnerabilities to investigate:** repeated nonce under the same GCM key, missing/ignored tag verification, too-short tag, mismatched AAD, incorrectly handled nonce lengths, replay of an otherwise valid authenticated message.

**Not an automatic bypass:** simply flipping ciphertext or changing an admin claim should be rejected by properly verified AEAD. GCM nonce reuse can cause serious confidentiality/authenticity problems but is **not** always solved by one XOR and a single packet.

**Toolkit:** `tools/block/aes_modes.py` and `tools/hash/hmac_basics.py` for authentication concepts; exercises B11/B12.

## 3.15 AES internal calculations / finite fields — [COURSE CONCEPT]

**Recognize it:** SubBytes, ShiftRows, MixColumns, AddRoundKey, key schedule, S-box, byte multiplication in `GF(2^8)`.

**Try:** add bytes with XOR, not ordinary addition; multiply polynomials modulo AES's irreducible polynomial `0x11B`; understand `xtime`, Rcon and 32-bit word operations.

**Toolkit:** `tools/block/aes_finite_fields.py`. These are **math exercises**, not proof that AES is broken.

---

# 4. HASH FUNCTIONS, SHA-1, SHA-2, SHA-3, MD5, PASSWORDS

## 4.1 Hashes are NOT encrypted messages — [COURSE CONCEPT]

`hash(message)` gives a digest; you normally cannot reverse SHA-256 like AES. If you see a hash and a tiny password dictionary, you can test guesses by hashing each candidate — that's **guessing**, not mathematically reversing SHA-256.

**Try first:** identify algorithm by challenge context, not hash length alone (different hashes may be truncated); inspect whether input is UTF-8 text, raw bytes, hex-decoded bytes, Base64-decoded bytes, or canonical JSON.

## 4.2 Collision vs preimage vs second preimage — [COURSE CONCEPT]

- **Collision:** find *any* two different messages with the same digest.
- **Preimage:** given a digest H, find *a message* whose hash is H.
- **Second preimage:** given a specific message, find a different message with its hash.

**Big warning:** a generic SHA-256 collision is NOT realistically solvable for a normal exam. If a challenge asks for one, look for **truncation, custom hashing, constrained input, or a deliberately weak algorithm**.

## 4.3 Truncated hash collision / birthday attack — [COURSE CONCEPT] [PAST CNS]

**Recognize it:** server saves just the first `n` bytes (or `k` hexadecimal characters) of a hash.

**Try:** generate many different valid messages, hash the exact canonical byte strings, and store `short_hash -> original_message`. When the same short hash occurs for two different messages, you found a collision.

**Rule of thumb:** if `b` bits remain, about `2^(b/2)` random tries for any collision (birthday effect). For a **specific** target digest, about `2^b` guesses.

**Watch:** 4 **bytes** = 32 bits; 4 **hex characters** = only 16 bits.

**Toolkit:** `12_secure_bank_2_short_hash_collision.py`.

## 4.4 Length-extension attacks — [COURSE CONCEPT + CTF / EXTRA]

**Recognize it:** a naive MAC looks like `SHA256(secret || message)` and you know its digest and the original message, but not the key.

**Try:** use the internal hash state encoded by the digest, guess secret length, add SHA-style `glue padding`, append new bytes, continue hashing. The forged message is often `original_message || glue_padding || suffix` (not pretty readable text).

**Needs:** a Merkle–Damgård construction with suitable state exposure (e.g. SHA-256, SHA-1, MD5); a vulnerable **secret-prefix MAC**; an API that accepts the resulting bytes.

**Does NOT apply directly to:** HMAC-SHA256, SHA3 sponge hashes, keyed BLAKE2 configured appropriately, or SHA256(`message || secret`) in the same simple form.

**Toolkit:** `tools/hash/sha256_length_extension.py`.

## 4.5 Custom home-made 'hash' that can be reversed — [CTF / EXTRA] [PAST CNS]

**Recognize it:** code changes every byte with XOR, rotate-left, XOR with previous byte, and rotates a list — but never destroys information or compresses the message.

**Try:** reverse operations **in reverse order**: reverse list rotation, undo XOR chain from right to left, rotate-right, undo XOR constant. Ordinary cryptographic hash functions intentionally discard information; a reversible byte scrambler does not.

**Toolkit:** `13_better_hash_reversing.py`.

## 4.6 Double hash / raw digest bytes vs digest hex — [CTF / EXTRA] [PAST CNS]

`SHA256(bytes.fromhex(previous_hex))` is DIFFERENT from `SHA256(previous_hex.encode())`.

```python
import hashlib
message = b"hello"
first = hashlib.sha256(message).digest()  # actual 32 digest bytes
second = hashlib.sha256(first).hexdigest()
print(second)
```

**Try:** when a challenge says "hash the hash", read whether they expect the binary digest bytes or the printable hexadecimal string.

**Toolkit:** `tools/hash/hash_functions.py`; `14_space_race_sha256_step.py`.

## 4.7 SHA-1 / MD5 weaknesses — [COURSE CONCEPT]

**Recognize it:** old or legacy hash used as a document fingerprint or collision-resistance mechanism.

**Try conceptually:** collisions are substantially weaker than with SHA-256. However, a random MD5/SHA-1 digest is not a password that can simply be reversed; practical collision construction is a specialised attack and depends on message constraints.

## 4.8 Password hashes: dictionary attack — [COURSE CONCEPT] [PAST CNS]

**Recognize it:** account hash, wordlist, captured challenge-response computed from password, or deliberately weak password storage.

**Try:** for each password candidate, compute the *exact same input bytes and hashing algorithm* used by the system. `password`, `salt+password`, `password+salt`, and `username:realm:password` are all different.

**Tip:** read wordlists in **binary mode** and strip only newline bytes (`rstrip(b"\r\n")`) so you don't change passwords unexpectedly.

**Toolkit:** `tools/hash/wordlist_hash_solver.py`, `tools/web/rtsp_digest_solver.py`.

## 4.9 Salts / PBKDF2 / scrypt — [COURSE CONCEPT + CTF / EXTRA]

**Salt:** usually public; prevents sharing the same hash across accounts and weakens precomputed rainbow-table reuse. It does **not** make a weak password unguessable.

**PBKDF2:** iterations slow each guess. **scrypt:** also costs memory. You must match hash name, salt bytes, iteration/work parameters, output length and encoding exactly.

**Do not assume:** a fixed salt guarantees security; too few iterations/weak passwords remain vulnerable to offline guessing.

## 4.10 SHA-3 / sponge / SHAKE — [COURSE CONCEPT]

**Recognize it:** Keccak sponge, `rate/capacity`, SHA3-256/512, SHAKE extensible-output hashes.

**Try for calculation:** follow absorb/squeeze phases and exact digest length. SHA3 is not simply SHA-256 with a different constant; its structure matters. The standard SHA-256 secret-prefix length-extension trick does **not** carry over unchanged.

---

# 5. MAC / HMAC / CMAC / JWT / JSON / NETWORK AUTHENTICATION

## 5.1 What HMAC does — [COURSE CONCEPT]

HMAC is a secret-key tag on **bytes**. To recompute a tag for changed bytes, you normally need the secret key. HMAC-SHA256 does not become forgeable just because the underlying SHA-256 has a length-extension property.

**Whenever you see a valid HMAC:** ask not just *"Can I forge it?"* but also *"Does the verifier check the same bytes that the application later uses?"*

**Toolkit:** `tools/hash/hmac_basics.py`.

## 5.2 JSON duplicate-key parser discrepancy — [CTF / EXTRA] [PAST CNS]

**Recognize it:** a signed JSON request is provided and the server verifies it, but the authenticated request and action might be parsed differently.

**Example of ambiguous raw JSON:**

```json
{"action":"view","role":"admin","role":"user"}
```

Some parsers keep the **last** `role`, while others take the **first**. The *same raw bytes* can then mean two different things to two components.

**What worked in your earlier CNS lab:** the order of duplicate keys mattered. A valid signature was reused while the two parts of the system appeared to disagree about which role applied. This is an **application/canonicalization bug**, not a break of SHA-256 or HMAC.

**Gotcha:** standard Python `json.loads()` silently keeps the last duplicate key. If you decode and re-encode JSON, duplicate keys will disappear. To test duplicates, keep a **raw JSON string** instead of reconstructing from a normal dict.

**Toolkit:** `tools/web/json_parser_tricks.py`; `16_signed_sealed_misinterpreted.py`.

## 5.3 Canonicalization mismatches in signed data — [CTF / EXTRA]

**Recognize it:** the server signs/compares a normalized JSON representation, but performs the operation on a differently parsed representation.

**Try checking:** duplicate keys, key order, whitespace, number types (`10` vs `10.0`), escaped Unicode, case sensitivity, trailing fields, URL decoding, and unexpected extra headers. A difference is useful only if it changes *what the application authorizes* while the signature verifier accepts it.

**Don't assume:** changing whitespace alone automatically bypasses a MAC. When both components normalize identically, it is safe.

## 5.4 JWT `alg: none` verification bug — [CTF / EXTRA] [PAST CNS]

**Recognize it:** token has 3 Base64url parts, `header.payload.signature`, and the header controls `alg`. It has a guest role and there is an admin endpoint.

**Try in a deliberately vulnerable training app:** decode the **header and payload**, change claims and examine whether the backend mistakenly accepts `alg=none` instead of enforcing an allowed algorithm. Some vulnerable apps have odd handling of the signature field; your earlier CNS example accepted a changed `alg`/role with the original signature retained.

**This is NOT normal JWT behaviour.** Correct verification requires a server-defined allowed algorithm, correct key and verified signature, regardless of untrusted token header suggestions.

**Toolkit:** `tools/web/jwt_for_beginners.py`; `17_token_of_trust_jwt.py`.

## 5.5 JWT algorithm/key confusion — [CTF / EXTRA]

**Recognize it:** application accepts both asymmetric and HMAC algorithms and chooses its verification method solely from the untrusted JWT header.

**Possible mistake:** code accidentally treats a public RSA verification key as an HMAC secret. This depends heavily on the library and key handling; it is **not** a universal JWT attack. Verify whether there is actual evidence of unsafe algorithm selection before attempting it.

## 5.6 Missing authentication vs authorization — [COURSE CONCEPT + CTF / EXTRA]

**Authentication:** who sent this? Is the signature valid? **Authorization:** is the signed request allowed to do `admin` operations? A perfectly valid HMAC on a user's `role=user` request should not grant admin actions.

**Try:** follow the data flow from **verified bytes** to **parsed object** to **authorization rule**. Bugs arise when those steps disagree.

## 5.7 Replay of an authenticated message — [CTF / EXTRA]

**Recognize it:** a valid signed request can be sent again, and there is no timestamp/nonce/sequence number (or no effective duplicate detection).

**Try:** assess whether the same authenticated action can be executed twice. HMAC proves origin/integrity, not uniqueness or freshness. The server must enforce replay protection separately.

## 5.8 MAC truncation — [COURSE CONCEPT + CTF / EXTRA]

**Recognize it:** server only compares a few MAC bytes.

**Risk:** guessing a valid tag takes about `2^b` tries for a `b`-bit tag, assuming uniformly random tags and no other weakness. Online rate limits, lockouts and tag lengths determine feasibility.

**Distinguish from hash collisions:** guessing a **specific MAC** does not benefit from the birthday collision shortcut in the same way.

## 5.9 CMAC vs naive CBC-MAC — [COURSE CONCEPT]

**Recognize it:** authentication tag computed using AES in a CBC-like chain.

**Try:** inspect whether the problem uses **proper CMAC** with last-block subkeys and specified padding, or a *naive* variable-length CBC-MAC. Naive CBC-MAC on arbitrary variable-length messages can be vulnerable to message-extension constructions; standard CMAC is designed to prevent that class of mistake.

**Do not infer:** AES-CBC encryption automatically provides a MAC. Encryption and authentication are separate properties.

## 5.10 RTSP/HTTP Digest Authentication — [CTF / EXTRA] [PAST CNS]

**Recognize it:** fields `username`, `realm`, `nonce`, `uri`, `method`, `response` in a network capture.

**For simple MD5 Digest without qop:**

```text
HA1 = MD5(username + ':' + realm + ':' + password)
HA2 = MD5(method   + ':' + uri)
response = MD5(HA1 + ':' + nonce + ':' + HA2)
```

**Try:** offline candidate passwords if a wordlist is provided. Ensure you use the exact method and URI and account for `qop`, `nc`, `cnonce`, and algorithm variants if present. A malformed input string will never match even with the right password.

**Toolkit:** `tools/web/rtsp_digest_solver.py`; `15_security_cam_rtsp_digest.py`.

## 5.11 AEAD / HMAC verification mistake — [COURSE CONCEPT + CTF / EXTRA]

**Recognize it:** application decrypts before verifying a tag, ignores tag verification errors, compares incorrect bytes, or signs one object but acts on another.

**Try:** trace which exact bytes are authenticated, what metadata is in AAD, and which decision is protected. **If a tag is verified correctly over all security-relevant data**, simple bit flipping should not pass.

---

# 6. Tiny Python recipes to copy during the exam

These are basic building blocks. The longer, commented solvers live in the matching folders.

```python
# RECIPE A: hex -> bytes -> readable text
raw = bytes.fromhex("636e737b746573747d")
print(raw.decode("utf-8"))  # cns{test}

# RECIPE B: XOR two aligned byte strings
from itertools import repeat
plain = bytes(x ^ y for x, y in zip(b"ABC", b"XYZ"))

# RECIPE C: split AES ciphertext into 16-byte blocks
ciphertext = bytes.fromhex("00112233445566778899aabbccddeeff" * 3)
blocks = [ciphertext[i:i + 16] for i in range(0, len(ciphertext), 16)]
for number, block in enumerate(blocks):
    print(number, block.hex())

# RECIPE D: create a CBC first-block IV modification
# Use real 16-byte inputs from the challenge, not these dummy example bytes.
def modify_cbc_iv(iv, original_plain_block, wanted_plain_block):
    assert len(iv) == len(original_plain_block) == len(wanted_plain_block) == 16
    return bytes(a ^ b ^ c for a, b, c in zip(iv, original_plain_block, wanted_plain_block))

# RECIPE E: detect repeated nonces in a JSON capture
from collections import defaultdict
by_nonce = defaultdict(list)
for packet in packets:                   # packets = list of JSON objects
    by_nonce[packet["nonce_hex"]].append(packet["id"])
for nonce, ids in by_nonce.items():
    if len(ids) > 1:
        print("Repeated nonce:", nonce, "packets:", ids)

# RECIPE F: find SHA-256 collisions on a SHORT prefix
import hashlib
fingerprint = hashlib.sha256(b"payment example").digest()[:4]
print(fingerprint.hex())

# RECIPE G: inspect duplicate JSON keys without losing them
import json
raw_json = '{"role":"admin","role":"user"}'
pairs = json.loads(raw_json, object_pairs_hook=lambda items: items)
print(pairs)  # [('role', 'admin'), ('role', 'user')]
```

**Note:** In Recipe E, `packets` must already contain the parsed JSON list from your capture. Recipe F only computes one short digest — the full collision search is in the toolkit. Recipe B demonstrates XOR, not an actual decryption.

---

# 7. The most important false friends — don't waste exam time

1. **"I have a SHA-256 hash, so I can decrypt it."** No. You can guess inputs or exploit a weak surrounding construction.
2. **"HMAC uses SHA-256, so length extension works."** No. HMAC construction prevents the simple secret-prefix length-extension attack.
3. **"JSON has duplicate keys, so HMAC is broken."** No. Only a real parsing/canonicalization mismatch might allow a bypass.
4. **"JWT says alg=none, so it always works."** No. Correct JWT servers reject unauthorised algorithms and invalid signatures.
5. **"Two CBC ciphertexts use the same IV, so XOR them to decrypt."** No. CBC is not a directly reusable XOR stream in the same way as CTR/OFB.
6. **"All AES modes let me swap ciphertext blocks."** No. Block splicing in the simple form applies to ECB and compatible block-aligned layouts.
7. **"AES-GCM is a stream cipher, so I can flip admin bytes."** Not if the authentication tag is verified properly.
8. **"Any 32-byte digest can be cracked with a birthday attack."** Not a given SHA-256 preimage. Birthday search is for *collisions* on unrestricted messages.
9. **"A 16-character hex nonce means 16 bytes."** No. Two hex characters encode one byte, so 16 hex chars = 8 bytes.
10. **"A ciphertext beginning with 42 4D must be a plaintext bitmap."** Maybe the BMP header is preserved; verify real file offsets before treating encrypted bytes as known plaintext.
11. **"The original plaintext length doesn't matter in a bit-flip attack."** It does. Changes must preserve exact byte alignment; stream bit flipping normally requires equal old/new lengths.
12. **"If the code runs, my cryptographic attack is proven."** No. Validate output with expected structure, multiple samples, server results or test vectors.

---

# 8. A plan for EVERY unknown CNS challenge

1. **Read the mission**: do I need a plaintext, a key, a forged valid request, a password, or a collision?
2. **Classify the input**: text, ciphertext, hash digest, JWT, signed JSON, binary file, protocol capture.
3. **Inspect data representation**: hex/Base64/bytes, nonce prefixes, 8-byte DES / 16-byte AES blocks, endian order, padding.
4. **Ask what you know**: exact plaintext? known prefix? repeated nonce? key generator? signature? public headers?
5. **Find the implementation mistake**, if any. Strong cryptography alone is usually not the weakness.
6. **Pick ONE testable hypothesis** from this playbook and its matching script.
7. **Run it on a tiny known example** before attacking the challenge input.
8. **Check output**: plausible UTF-8, correct prefix, JSON structure, block padding, signed response, or official flag checker.
9. **If it fails**, check wrong mode, offsets, key/nonce, representation, counter start, or your assumptions. Do not immediately invent a new vulnerability.
10. **Document the working idea** in 2–3 sentences so you can repeat it alone during the exam.

### Find these files quickly

- `WHAT_SHOULD_I_TRY.md` — original short decision guide.
- `OPEN_THIS_DURING_EXAM.md` — new 30-second lookup.
- `tools/basics/`, `tools/stream/`, `tools/block/`, `tools/hash/`, `tools/web/` — reusable Python helpers.
- `past-exercises/` — your 17 earlier solved challenges.
- `TESTS/` — offline sanity checks.

**Use only on the authorized CNS practice/lab environment.**


---

# 9. READY-TO-RUN PYTHON RECIPES (copy the commands, change the values)

All recipes below are actual files under `tools/recipes/` and work with Linux/Ubuntu.
Run the commands **from the repository root**. To list an individual tool's options, add `--help`.
The exercises and your old solutions have fuller examples in `practice/` and `past-exercises/`.

## 9.1 Same keystream, known plaintext (Salsa20, ChaCha20, AES-CTR, OTP)

**When to try:** two messages have the same key+nonce+counter start (or a provably matching keystream interval), and the plaintext of one message is known.

```bash
python3 -m tools.recipes.xor_reuse \
  --known 'STATUS: OK' \
  --known-cipher 00010203040506070809 \
  --secret-cipher 1112131415161718191a
```

Here the values are *demonstration bytes*, not an actual challenge. The program outputs recovered bytes and their hex representation. If the unknown message begins at a different counter (ChaCha20 S05), **align the keystream using `offset_bytes = (counter2-counter1) * 64`**, not starting at index zero. Compare `practice/round_03/exercise_01_stream_S05/solution.py`.

### Why XOR works (the 3 lines to remember)

- `known_cipher = known_plain XOR stream`
- `stream = known_cipher XOR known_plain`
- `secret_plain = secret_cipher XOR stream`

If you have only 20 known plaintext bytes, you can decrypt only the corresponding 20 bytes of the other ciphertext. `zip()` silently truncates; compare lengths before assuming you have the whole message.

## 9.2 Bit flip an unauthenticated encrypted value

**When to try:** you know the old bytes inside ciphertext and want to change the same byte positions without the key. The cipher is a stream mode without a valid authentication tag.

```bash
python3 -m tools.recipes.stream_bitflip \
  --cipher-hex 1020304050607080 \
  --offset 0 \
  --old 'amount=1' \
  --new 'amount=9'
```

The two replacements must have the same UTF-8 byte length. For a nonce-prefixed packet, **strip the nonce before choosing an offset**, or add the nonce length to the offset if editing the whole packet. See `past-exercises/08_secure_bank/`.

## 9.3 AES-ECB: replace one 16-byte encrypted block

**When to try:** ECB encrypts independent blocks and the application accepts fields at fixed block positions. You have a donor block already encrypted under the SAME key.

```bash
python3 -m tools.recipes.ecb_splice \
  --cipher 0000000000000000000000000000000011111111111111111111111111111111 \
  --block-index 1 \
  --replacement 22222222222222222222222222222222
```

This is not forging an AES encryption of a new plaintext. It is rearranging ciphertext blocks. A secure MAC/tag should prevent the final message from being accepted.

## 9.4 AES-CBC: manipulate FIRST block with IV

**When to try:** CBC mode; attacker controls IV; knows old first plaintext block; wants equal-length new first plaintext block.

```bash
python3 -m tools.recipes.cbc_iv \
  --iv 000102030405060708090a0b0c0d0e0f \
  --old 'access=guest;pad' \
  --new 'access=admin;pad'
```

`IV_new = IV_old XOR old_plain XOR desired_plain`.

**Different challenge:** for an INNER block, alter the preceding ciphertext block and accept that the previous plaintext block may become corrupted. If IV is not editable, use the `B05` concept, not the above equation blindly.

## 9.5 Hash a password correctly: raw digest vs hex text

```bash
python3 -m tools.recipes.hash_dictionary \
  --wordlist practice/round_01/exercise_03_hash_H02/candidate_passwords.txt \
  --target 7e41ad40c564bed5789af1eb4e8b8ec893d8d5d4c7367c6913e96b0a219ada6e \
  --mode sha256-hex-text-twice
```

`sha256(sha256(password).digest())` and `sha256(sha256(password).hexdigest().encode())` are different! The inner `.digest()` is 32 raw bytes; `.hexdigest().encode()` is 64 ASCII bytes. Match the service's exact code.

## 9.6 Find collisions in short hash prefixes

```bash
python3 -m tools.recipes.short_hash_collision --prefix-bytes 3
```

For a 24-bit digest, collisions are expected after roughly `2^12` attempts by the birthday effect; that does not mean SHA-256 itself has a practical full collision break.

## 9.7 SHA256(secret || message) length extension

```bash
python3 -m tools.recipes.sha256_extend \
  --digest 3361342b2acbeb71eeca7b83776cd019e0c58e3a42ea616e6ff3064da48127a7 \
  --message 'file=report.txt&role=reader' \
  --append '&role=supervisor' \
  --secret-length 9
```

Try all plausible secret lengths and **send the raw forged bytes**, not a human-readable literal containing `\x80`. This technique does **not** break HMAC-SHA256 or SHA-3. See `practice/round_02/exercise_03_hash_H06/solution.py` for length guessing.

## 9.8 Signed JSON parser confusion / duplicate keys

```bash
python3 -m tools.recipes.json_duplicates --key role --first admin --last user
```

Python's regular `json.loads()` keeps the LAST duplicate, but another parser might keep the FIRST. A signature might be valid for the last value while authorization uses the first. This is a **parser discrepancy**, not a cryptographic forgery. Some validators reject duplicate keys. For nested JSON inspect `practice/round_01/exercise_04_mac_M04/solution.py`.

**Never serialize duplicate keys using a Python `dict`**: a dict can hold only one value for each key. Build the raw JSON text (or carefully use a list of key-value pairs).

## 9.9 JWT `alg: none` demonstration for broken validators only

```bash
python3 -m tools.recipes.jwt_none \
  --token "$(cat practice/round_02/exercise_04_mac_M03/guest_jwt.txt)" \
  --role admin
```

A correct JWT library must NOT accept this unless an unsigned token is explicitly allowed in the application policy. **Important variant:** in one past CNS lab the old signature was retained, whereas the new M03 practice expects an EMPTY third segment. Read the exact validation behavior!

## 9.10 RTSP/HTTP Digest with qop=auth

```bash
python3 practice/round_03/exercise_04_mac_M02/solution.py
```

- No qop: `MD5(HA1:nonce:HA2)`.
- With qop=auth: `MD5(HA1:nonce:nc:cnonce:qop:HA2)`.
- `HA1=MD5(username:realm:password)`; `HA2=MD5(method:uri)`.

Wrong method or URI means wrong response even with the correct password. Handle wordlists as raw bytes when possible.

## 9.11 DES with constrained keys / double AES meet-in-the-middle

**When to try:** DES key has a known `IOTDEV` prefix and only two unknown bytes; or AES 2 uses tiny keys with two encryptions.

- DES original and cleaned code: `past-exercises/09_des_iotdev/`.
- Double AES reference: `past-exercises/11_aes2/` (20-bit sides, heavy).
- Fast double AES practice: `practice/round_03/exercise_02_block_B10/solution.py` (12-bit sides).

Use PyCryptodome or `cryptography`. **A full 128-bit AES key is not brute-forceable**. These tasks become feasible only because the developer reduced the secret key space.

---

# 10. More attack recognition traps — exam checklist

| If the challenge mentions ... | Check this FIRST | Why a naive approach fails |
|---|---|---|
| `nonce` reused for CBC | Mode is CBC, not CTR | XOR two CBC ciphertexts does NOT recover the two plaintext XORs |
| Salsa20/CTR with nonce prefix | Are the nonce bytes INCLUDED in the given hex? | Shifting offsets by 8 or 12 bytes breaks the XOR attack |
| ChaCha20 different start blocks | Counter alignment | Shared key+nonce alone does not mean first keystream byte aligns |
| ECB fixed-size JSON fields | Boundaries at 16 bytes | Splicing mid-block bytes corrupts blocks |
| CBC bitflip of block i | Whether corrupted previous block is tolerated | Changing C_(i-1) also scrambles P_(i-1) |
| GCM/CCM 'change ciphertext' | Is authentication verified? | Wrong tag causes rejection; encryption alone is not enough |
| `pad` / `unpad` exceptions | PKCS#7 padding and oracle visibility | Padding oracle needs distinguishable error signals |
| SHA-256 digest unknown input | Preimage vs collision | Birthday bound helps collisions, not arbitrary preimages |
| SHA-256(secret + message) | Prefix vs HMAC | Only secret-prefix Merkle–Damgård construction is length-extensible |
| `hexdigest()` used before next hash | 64 ASCII bytes vs 32 raw bytes | Wrong digest representation changes the hash |
| JWT 3 dot-separated chunks | Base64url decoding of each individually | Padding is different per section, signatures are not plain JSON |
| Signed JSON valid yet different behavior | Duplicate keys, normalization, case, data types | MAC proves the signed representation, not necessarily the authorized interpretation |
| RTSP Digest | qop, nc, cnonce, method, URI | Omitting one field prevents a candidate match |
| `nc` server returns no banner | TCP protocol may wait for your input | Do not treat silence as a connection failure |
| Secret value appears inside ciphertext | Is it actually encrypted or just hex/Base64? | Convert encodings before attempting cryptography |

**Safety:** apply these to your course lab or your own systems. This playbook documents common implementation weaknesses; it does not imply that AES, SHA-256 or HMAC are generally broken.


## Verified directory links to previous exercises

This section links to the existing folders in the repository (rather than placeholder names).

| Attack pattern | Old CNS exercise |
|---|---|
| Caesar | [01 Caesar](../past-exercises/01_caesar/solution.py) |
| Substitution | [02 Switcheroo](../past-exercises/02_switcheroo/solution.py) |
| Vigenère | [03 French Vigenère](../past-exercises/03_french_vigenere/solution.py) |
| Letter frequency | [04 Count Letters](../past-exercises/04_count_letters/solution.py) |
| XOR | [05 Dutch XOR](../past-exercises/05_dutch_xor/solution.py) |
| Rotor / Enigma | [06 Enigma](../past-exercises/06_enigma/solution.py) |
| Weak pseudo-random generator | [07 Replanting](../past-exercises/07_replanting/solution.py) |
| **Stream ciphertext bitflipping** | **[08 Secure Bank](../past-exercises/08_secure_bank/solution.py)** |
| Limited DES keyspace | [09 DES IoT Device](../past-exercises/09_des_iotdev/solution.py) |
| Nonce reuse | [10 Noncense](../past-exercises/10_noncense/solution.py) |
| Meet-in-the-middle | [11 AES2](../past-exercises/11_aes2/solution.py) |
| Secure Bank follow-up | [12 Secure Bank 2](../past-exercises/12_secure_bank_2/solution.py) |
| Weak hash | [13 Better Hash](../past-exercises/13_better_hash/solution.py) |
| Hash-related challenge | [14 Space Race](../past-exercises/14_space_race/solution.py) |
| RTSP Digest | [15 Security Cam](../past-exercises/15_security_cam/solution.py) |
| HMAC/JSON | [16 HMAC JSON](../past-exercises/16_hmac_json/solution.py) |
| JWT | [17 JWT](../past-exercises/17_jwt/solution.py) |
