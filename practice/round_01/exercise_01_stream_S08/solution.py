"""S08: decrypt a private stream-cipher message when a nonce repeats.

Why? In Salsa20, same secret key + same nonce + same initial position
produce the SAME XOR keystream. We do NOT break the Salsa20 algorithm.

Try before reading this file: compare the nonce_hex strings in packets.json.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

def xor_bytes(first, second):
    """XOR two byte strings; stop when the shorter one ends."""
    result = bytearray()
    for byte_a, byte_b in zip(first, second):
        result.append(byte_a ^ byte_b)
    return bytes(result)

def main():
    packets = json.loads((HERE / "packets.json").read_text())
    known_plaintext = (HERE / "public_message.bin").read_bytes()

    # Make a dictionary of nonce -> packets using that nonce.
    groups = {}
    for packet in packets:
        nonce = packet["nonce_hex"]
        groups.setdefault(nonce, []).append(packet)

    # Only inspect pairs with duplicate nonce values.
    for nonce, same_nonce_packets in groups.items():
        if len(same_nonce_packets) < 2:
            continue
        print("Repeated nonce:", nonce)

        # This exercise identifies the public ciphertext by matching the
        # length of the known plaintext (195 bytes).
        for known_packet in same_nonce_packets:
            known_cipher = bytes.fromhex(known_packet["ciphertext_hex"])
            if len(known_cipher) != len(known_plaintext):
                continue
            for private_packet in same_nonce_packets:
                if private_packet is known_packet:
                    continue
                private_cipher = bytes.fromhex(private_packet["ciphertext_hex"])
                keystream = xor_bytes(known_plaintext, known_cipher)
                recovered = xor_bytes(private_cipher, keystream)
                print("Public packet:", known_packet["id"])
                print("Private packet:", private_packet["id"])
                print("Recovered:", recovered.decode("utf-8", errors="replace"))

                # The challenge wants only the value after this label.
                if b"RELAY CONTROL KEY=" in recovered:
                    answer = recovered.split(b"RELAY CONTROL KEY=", 1)[1]
                    answer = answer.split(b";", 1)[0].strip()
                    print("SUBMIT:", answer.decode())
                    return

    print("No matching message found. Check the plaintext and the packet format.")

if __name__ == "__main__":
    main()
