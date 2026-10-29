"""Quick self-test for Python byte, cipher and hash fundamentals.

Run from the repository root:
    python3 smoke_test.py

Does not contact external services or require pip packages.
"""
import hashlib
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def xor(a: bytes, b: bytes) -> bytes:
    if len(a) != len(b):
        raise ValueError("XOR operands should have equal length in this test")
    return bytes(x ^ y for x, y in zip(a, b))

def main() -> int:
    assert bytes.fromhex("68656c6c6f") == b"hello"
    assert hashlib.sha256(b"abc").hexdigest() == (
        "ba7816bf8f01cfea414140de5dae2223"
        "b00361a396177a9cb410ff61f20015ad"
    )
    known = b"hello"
    stream = b"abcde"
    known_cipher = xor(known, stream)
    secret = b"world"
    assert xor(xor(secret, stream), xor(known, known_cipher)) == secret
    print("[PASS] byte encoding, SHA-256, XOR reused-keystream")

    for module in (
        "tools.recipes.xor_reuse",
        "tools.recipes.stream_bitflip",
        "tools.recipes.cbc_iv",
        "tools.recipes.hash_dictionary",
        "tools.recipes.jwt_none",
    ):
        result = subprocess.run(
            [sys.executable, "-m", module, "--help"],
            cwd=ROOT, capture_output=True, text=True, check=False
        )
        if result.returncode != 0:
            print(f"[FAIL] {module}\n{result.stderr}")
            return 1
        print(f"[PASS] {module} CLI")
    print("All basic checks passed. Some exercises may need optional packages or live course services.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
