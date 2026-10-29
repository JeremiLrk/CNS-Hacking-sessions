"""[EXTRA] ENCODING — used in almost every CNS exercise.

Encoding is like spelling the SAME information in another way.
It is NOT encryption. You do not need a secret to reverse it.

WHEN TO OPEN THIS FILE:
- A server gives hex, Base64, Base64url, URL-encoded text, numbers or bytes.
- You do not know whether your SHA / XOR / AES input is TEXT or BYTES.
"""
import base64
from urllib.parse import quote, unquote


def text_to_bytes(text):
    # Computer cryptography works on bytes, not normal Python strings.
    return text.encode("utf-8")


def hex_to_bytes(hex_text):
    # Example: "4142" -> b"AB" (TWO bytes).
    return bytes.fromhex(hex_text)


def bytes_to_hex(data):
    # Example: b"AB" -> "4142".
    return data.hex()


def base64_decode(text):
    # Standard Base64: often ends with = or ==.
    missing_equals = (-len(text)) % 4
    text = text + "=" * missing_equals
    return base64.b64decode(text)


def base64_encode(data):
    return base64.b64encode(data).decode("ascii")


def base64url_decode(text):
    # JWT uses URL-safe Base64. It often removes the equals signs.
    text += "=" * (-len(text) % 4)
    return base64.urlsafe_b64decode(text)


def base64url_encode(data):
    return base64.urlsafe_b64encode(data).decode("ascii").rstrip("=")


def integer_to_bytes(number, size=4, order="big"):
    # big = biggest byte first; little = smallest byte first.
    return number.to_bytes(size, order)


def bytes_to_integer(data, order="big"):
    return int.from_bytes(data, order)


def show_bytes(data):
    # Useful if bytes are NOT readable text (common in encrypted data).
    print("Raw bytes: ", repr(data))
    print("Hex:       ", data.hex())
    print("Length:    ", len(data), "bytes")
    print("Text:      ", data.decode("utf-8", errors="replace"))


if __name__ == "__main__":
    print("Why b'4142' and bytes.fromhex('4142') are DIFFERENT:")
    show_bytes(b"4142")  # 4 bytes: the characters '4','1','4','2'.
    show_bytes(bytes.fromhex("4142"))  # 2 bytes: the letters 'A','B'.
    assert hex_to_bytes("4142") == b"AB"
    assert base64_decode(base64_encode(b"hello")) == b"hello"
    assert base64url_decode(base64url_encode(b"hello")) == b"hello"
    assert unquote(quote("hi there")) == "hi there"
