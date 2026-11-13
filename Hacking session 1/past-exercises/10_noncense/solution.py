"""NONCENSE — known plaintext + AES-CTR nonce reuse.

WHEN TO TRY: Two messages use the SAME keystream.
The cipher does not matter if both are XOR stream style:
   C1 = P1 XOR K
   C2 = P2 XOR K
Therefore P2 = P1 XOR C1 XOR C2.

You do NOT need the AES secret key!
BUT: this only recovers as many bytes as you know of P1.
"""

from pathlib import Path

DATA = Path(__file__).resolve().parent / "data"


def recover_message(known_plaintext, known_ciphertext, target_ciphertext):
    output = bytearray()
    readable_length = min(len(known_plaintext), len(known_ciphertext), len(target_ciphertext))
    for index in range(readable_length):
        byte = known_plaintext[index] ^ known_ciphertext[index] ^ target_ciphertext[index]
        output.append(byte)
    return bytes(output)


def main():
    known_plaintext = (DATA / "known_message.txt").read_bytes().rstrip(b"\r\n")
    known_ciphertext = bytes.fromhex((DATA / "ciphertext_known.hex").read_text().strip())
    target_ciphertext = bytes.fromhex((DATA / "ciphertext_flag.hex").read_text().strip())
    print("Decrypted message:", recover_message(known_plaintext, known_ciphertext, target_ciphertext).decode())


if __name__ == "__main__":
    main()
