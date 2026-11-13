# CHAPTER 2 — Symmetric Encryption

[HOME](../README.md) · [EXAM CHEATSHEET](EXAM_CHEATSHEET.md)

## How to recognize the trick

| Given | Consider | Important condition |
|---|---|---|
| Stream cipher, reused nonce | Keystream reuse | Same key, counter and alignment |
| Alter encrypted JSON amount | Bitflipping | XOR stream without authentication |
| AES ECB | Repeated blocks or swapping | Same key and exact 16-byte alignment |
| CBC, editable IV | Change first plaintext block | Known original first block; no MAC |
| DES mostly fixed key | Brute-force unknown bytes | Verify key format, padding, mode |
| Two small-key encryption layers | Meet-in-the-middle | Reliable known plaintext/ciphertext pair |

## Formula + code: keystream reuse

`C = P XOR S`. Thus `S = C1 XOR P1` and `P2 = C2 XOR S`.

```python
xor = lambda a,b: bytes(x^y for x,y in zip(a,b))
known_plain = b"hello"
known_cipher = bytes.fromhex("09070f0d0e")
secret_cipher = bytes.fromhex("160d130d05")
stream = xor(known_plain,known_cipher)
print(xor(secret_cipher,stream))
```

Terminal recipe:
```bash
python3 -m tools.recipes.xor_reuse --known "hello" --known-cipher 09070f0d0e --secret-cipher 160d130d05
```

## Formula + code: stream bitflip

`C' = C XOR old XOR wanted` at the **correct offset**. New and old bytes must have equal length.

```python
cipher = bytearray.fromhex("010203040506")
offset = 1
old,new = b"abc",b"xyz"
for i in range(len(old)):
    cipher[offset+i] ^= old[i] ^ new[i]
print(cipher.hex())
```

## Formula + code: CBC IV

`IV_new = IV_old XOR old_P1 XOR wanted_P1`. AES-CBC uses a **16-byte IV**.

```python
iv = bytes.fromhex("00"*16)
old = b"role=user;id=001"
new = b"role=root;id=001"
assert len(old)==len(new)==16
print(bytes(x^a^b for x,a,b in zip(iv,old,new)).hex())
```

More: [Nonce reuse](../tools/stream/nonce_reuse_solver.py) · [AES modes](../tools/block/aes_modes.py) · [DES](../tools/block/des_small_key_solver.py) · [Double AES](../tools/block/double_aes_mitm.py)

Previous exercises: [Secure Bank](../past-exercises/08_secure_bank/solution.py) · [DES](../past-exercises/09_des_iotdev/solution.py) · [Noncense](../past-exercises/10_noncense/solution.py) · [AES2](../past-exercises/11_aes2/solution.py) · [Secure Bank 2](../past-exercises/12_secure_bank_2/solution.py)

**No authentication = possible tampering; correctly checked MAC/AEAD should reject it.**


## Links to previously solved exercises

| Attack | When to use it | Previous exercise and code |
|---|---|---|
| **Stream-cipher bitflipping** | Change a known plaintext field without the stream key (unauthenticated ciphertext) | **08 Secure Bank** — [solution.py](../past-exercises/08_secure_bank/solution.py) |
| **Nonce/keystream reuse** | Known plaintext and another ciphertext under same keystream | **10 Noncense** — [solution.py](../past-exercises/10_noncense/solution.py) |
| **Weak PRNG stream** | Predict stream from home-made random generator | **07 Replanting** — [solution.py](../past-exercises/07_replanting/solution.py) |
| **Reduced DES keyspace** | Brute force a few unknown key bytes | **09 DES IoT Device** — [solution.py](../past-exercises/09_des_iotdev/solution.py) |
| **Double AES / meet-in-the-middle** | Small independent keys in two encryption layers | **11 AES2** — [solution.py](../past-exercises/11_aes2/solution.py) |
| **Transaction manipulation (variant)** | Study the second bank challenge separately | **12 Secure Bank 2** — [solution.py](../past-exercises/12_secure_bank_2/solution.py) |

The CBC IV and ECB cut-and-paste examples also have [practice B04](../practice/round_02/exercise_02_block_B04/challenge.md) and [practice B03](../practice/round_01/exercise_02_block_B03/challenge.md); these are **new practice exercises**, not falsely labelled as past CNS exercises.
