# Python words explained like you are learning Python today

When you open a script and a line looks confusing, search for it here.

## 1. `b"hello"` vs `"hello"`

- `"hello"` is a Python string (readable text).
- `b"hello"` is a list-like sequence of byte values (what ciphers actually use).
- `"hello".encode()` converts text into bytes.
- `b"hello".decode()` converts those bytes back to text.

## 2. `.hex()` and `bytes.fromhex()`

```python
raw = b"AB"
print(raw.hex())              # 4142
print(bytes.fromhex("4142"))  # b'AB'
```

## 3. `.digest()` vs `.hexdigest()`

```python
import hashlib
h = hashlib.sha256(b"hello")
print(h.digest())     # 32 raw bytes (may look like unreadable characters)
print(h.hexdigest())  # 64 readable hex digits
```

## 4. `zip(a,b)`

Puts items from two lists/byte sequences into pairs:

```python
for left, right in zip(b"AB", b"CD"):
    print(left, right)
```

The first pair is the numeric byte value of A and C. `zip` STOPS when either input ends!
This is handy for partial known-plaintext attacks, but check lengths when full alignment matters.

## 5. `enumerate(items)`

Adds a position number:

```python
for index, letter in enumerate("ABC"):
    print(index, letter)
# 0 A
# 1 B
# 2 C
```

## 6. `%` (modulo)

Gives the remainder after division. Example: `7 % 3 == 1`.
We use `% len(key)` to repeat a short key.

## 7. `^` (XOR)

Bitwise XOR between integers. Example: `3 ^ 3 == 0`.
It is not 'to the power of' in Python (that is `**`).

## 8. `bytearray(data)`

A `bytes` object cannot be edited in place, but `bytearray` CAN.
So we often do `copy=bytearray(ciphertext)` then edit `copy[i]`.

## 9. `.rstrip(b"\r\n")`

Remove the newline at the end of a password-list entry, while keeping any spaces that may be part of the password.

## 10. `with open(...,"rb") as file:`

Open file as **raw bytes** (`rb`). Python closes the file automatically after the `with` block.
Important for password wordlists and binary files.

## 11. `raise ValueError(...)`

Stop execution because the input is not suitable. Better than producing a nonsense result.

## 12. `assert something`

Test that an expected result is true. If false, Python reports an error. Our `TESTS` folder uses this to catch mistakes.
