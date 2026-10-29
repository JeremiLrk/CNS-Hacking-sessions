"""DUTCH BAKERS — XOR ciphertext with a given hexadecimal key.

WHEN TO TRY: You receive long hex values and a hex key.
Remember: two hex characters = one byte. Use bytes.fromhex(), NOT .encode().

If key and data are the same length, XOR one byte with one key byte.
If the key is shorter, repeating XOR is a reasonable CTF hypothesis.
"""

CIPHERTEXT_HEX = (
    "555c4d461054524145590c45434045445353525a55400d544f5153425945"
    "55535342564f47165353514f5b455542065253594e534d5753434b4500"
    "43471649434e49454548535445454243591652455043585e5047104552"
    "4e585d544150525d16455111525e4d595f15545f5042571754555c55"
    "444245550a4d421154534a45585f45434145445e53570755455a544e"
    "5d53435a4554035342054f42425352544f5b4155425352535b4e5317"
    "5752414b4401"
)
KEY_HEX = "636f6d7075746572656e6e65747765726b7365637572697479697374686562657374636f75727365"

# The original copied problem text had a stray '1' after the final hex.
# More importantly the copied ciphertext may have an odd number of hex digits.
# DON'T invent a nibble: validate it and inspect the original prompt if needed.


def xor_repeating(data, key):
    if not key:
        raise ValueError("Key is empty")

    output = bytearray()
    for index in range(len(data)):
        output.append(data[index] ^ key[index % len(key)])
    return bytes(output)


def main():
    try:
        ciphertext = bytes.fromhex(CIPHERTEXT_HEX)
    except ValueError:
        print("The copied ciphertext has odd/invalid hex length.")
        print("Check the text against the original challenge before changing it.")
        return

    key = bytes.fromhex(KEY_HEX)
    print("Key as text:", key.decode("utf-8", errors="replace"))
    layer1 = xor_repeating(ciphertext, key)
    print("First XOR layer (ASCII hex):", layer1)

    # The XOR result contains HEX TEXT, not the final readable message.
    # Normally you can now decode that text using bytes.fromhex().
    try:
        plaintext = bytes.fromhex(layer1.decode("ascii"))
        print("Decoded message:", plaintext.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        print("The first layer is corrupted around byte 87.")
        print("The supplied ciphertext appears to be missing one byte.")

        # TEST A REPAIR HYPOTHESIS for THIS uploaded example only.
        # The missing byte makes the key alignment one position wrong.
        # Change the key alignment AFTER that byte to test the hypothesis.
        first_part = layer1[:87]
        later_part = bytearray()
        for index in range(87, len(ciphertext)):
            correct_key_index = (index + 1) % len(key)
            later_part.append(ciphertext[index] ^ key[correct_key_index])

        # We can see a single '7' before the gap: one missing '7' would
        # complete the ASCII hex code '77', which represents letter 'w'.
        # This is INFERRED FROM THE PATTERN, not recovered with certainty.
        possible_hex_text = first_part + b"7" + bytes(later_part)
        try:
            guess = bytes.fromhex(possible_hex_text.decode("ascii"))
            print("Possible reconstructed message:")
            print(guess.decode("utf-8", errors="replace"))
            print("WARNING: verify against the uncorrupted original ciphertext.")
        except (ValueError, UnicodeDecodeError):
            print("The repair hypothesis did not give valid hex text.")


if __name__ == "__main__":
    main()
