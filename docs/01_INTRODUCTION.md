# CHAPTER 1 — Introduction / Classic ciphers

[HOME](../README.md) · [EXAM CHEATSHEET](EXAM_CHEATSHEET.md)

## Recognize and solve

1. **Caesar:** one consistent letter shift → brute-force 26 shifts.
2. **Substitution:** arbitrary alphabet mapping → reverse the map to decrypt, use letter frequency/word shapes.
3. **Vigenère:** repeating keyword → subtract key shifts; check whether punctuation advances the key.
4. **Enigma/rotors:** track rotor positions, step timing and inverse mappings.
5. **XOR:** plaintext/ciphertext bytes and key → `P = C ^ K`.
6. **Hex/Base64:** decode first; neither is encryption.

## Tiny usable Python

```python
# Caesar decryption: try all possibilities
cipher = "KHOOR"
for shift in range(26):
    out = "".join(chr((ord(c)-65-shift)%26+65) if "A"<=c<="Z" else c for c in cipher)
    print(shift, out)
```

```python
# Repeat XOR key, preserve raw bytes
cipher = bytes.fromhex("09070f")
key = b"key"
plain = bytes(c ^ key[i % len(key)] for i,c in enumerate(cipher))
print(plain)
```

## Study real solutions

[Caesar](../past-exercises/01_caesar/solution.py) · [Switcheroo](../past-exercises/02_switcheroo/solution.py) · [Vigenère](../past-exercises/03_french_vigenere/solution.py) · [Frequency analysis](../past-exercises/04_count_letters/solution.py) · [XOR](../past-exercises/05_dutch_xor/solution.py) · [Enigma](../past-exercises/06_enigma/solution.py)

[Python syntax](PYTHON_BASICS.md) · [Terminal](UBUNTU_TERMINAL.md)
