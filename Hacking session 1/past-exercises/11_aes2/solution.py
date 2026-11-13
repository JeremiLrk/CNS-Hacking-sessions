"""AES 2 DEMO — your working meet-in-the-middle approach, explained simply.

STATUS: SOLVED BY YOU (user-confirmed).
THIS FILE'S TEST STATUS: The full 2^20 search was not rerun by the assistant.
Those two facts are different. Your solution is NOT being called unsuccessful.

WHY THIS ATTACK WORKS
---------------------
The service encrypts the data TWICE:
    P --AES with K1--> MIDDLE --AES with K2--> C

The keys are only 20 bits each. Trying every PAIR would take 2^40 tries.
Instead:
  1. Try all K1 values and remember the MIDDLE result.
  2. Try every K2 backwards, looking for the SAME middle result.
  3. Decrypt the promo code using both keys, in reverse order.

IMPORTANT ABOUT THE BMP
-----------------------
Your ORIGINAL working code used bytes 54..69 as the ciphertext block,
and a specifically chosen 16-byte known-plaintext candidate.
I preserve those EXACT values. Don't silently change offset 54 to the
BMP header's pixel-data offset (138): they are different questions.

Need: pip install pycryptodome
Run the full key search explicitly with: python 11_aes_2_meet_in_the_middle.py --run
WARNING: 2^20 AES operations on both sides take substantial CPU and memory.
"""

import sys
from pathlib import Path

DATA_FOLDER = Path(__file__).resolve().parent / "data"
NUMBER_OF_KEYS = 2 ** 20

# Copy of the known plaintext block chosen in YOUR original solution.
# Exactly 16 bytes long: AES works on 16-byte blocks.
KNOWN_PLAINTEXT = bytes.fromhex(
    "0000ff00"
    "00ff0000"
    "ff000000"
    "000000ff"
)

# These are the bytes your uploaded code used from the encrypted BMP.
CIPHERTEXT_OFFSET = 54

# The actual promo ciphertext supplied in the exercise.
PROMO_HEX = (
    "df7c7dfbd5e1ba2af108d658132d5f20d34de27da16375ceabd7a79cbfe738244"
    "027a4a0b26ec498a2c223a545b9567c20bf423bb38514e6cd6f043ab9e23a84"
    "ffa6745294c224068e1cffd9e8c9e294"
)


def full_key(small_number):
    """Turn a 20-bit number into the required 16-byte AES key."""
    first_three_bytes = small_number.to_bytes(3, "big")
    thirteen_zero_bytes = b"\x00" * 13
    return first_three_bytes + thirteen_zero_bytes


def find_key_pairs(known_plaintext, matching_ciphertext, key_limit=NUMBER_OF_KEYS):
    """Yield any key pair where both encryption directions meet in the middle."""
    from Crypto.Cipher import AES

    if len(known_plaintext) != 16 or len(matching_ciphertext) != 16:
        raise ValueError("Provide ONE 16-byte plaintext and ciphertext block")

    # PHASE 1: encrypt the known block using EVERY possible first key.
    # Instead of just storing the ciphertext, save which key produced it.
    middle_to_first_key = {}
    for first_number in range(key_limit):
        first_cipher = AES.new(full_key(first_number), AES.MODE_ECB)
        middle = first_cipher.encrypt(known_plaintext)
        middle_to_first_key[middle] = first_number

    # PHASE 2: decrypt the matching ciphertext with each possible second key.
    # A matching middle value tells us which two keys to try together.
    for second_number in range(key_limit):
        second_cipher = AES.new(full_key(second_number), AES.MODE_ECB)
        middle = second_cipher.decrypt(matching_ciphertext)
        if middle in middle_to_first_key:
            first_number = middle_to_first_key[middle]
            yield first_number, second_number


def decrypt_twice(ciphertext, first_number, second_number):
    """Undo K2 FIRST, then K1, because encryption used K1 then K2."""
    from Crypto.Cipher import AES

    second_cipher = AES.new(full_key(second_number), AES.MODE_ECB)
    after_second_layer = second_cipher.decrypt(ciphertext)

    first_cipher = AES.new(full_key(first_number), AES.MODE_ECB)
    plaintext_with_padding = first_cipher.decrypt(after_second_layer)
    return plaintext_with_padding


def main():
    bmp = (DATA_FOLDER / "enc.bmp").read_bytes()
    matching_ciphertext = bmp[CIPHERTEXT_OFFSET:CIPHERTEXT_OFFSET + 16]
    print("Known plaintext:", KNOWN_PLAINTEXT.hex())
    print("Matching BMP bytes at offset 54:", matching_ciphertext.hex())

    if "--run" not in sys.argv:
        print("To run your original full key search, add --run")
        return

    from Crypto.Util.Padding import unpad
    promo = bytes.fromhex(PROMO_HEX)

    for first_number, second_number in find_key_pairs(
        KNOWN_PLAINTEXT, matching_ciphertext
    ):
        print("Possible key 1:", first_number)
        print("Possible key 2:", second_number)
        print("Full key 1:", full_key(first_number).hex())
        print("Full key 2:", full_key(second_number).hex())

        # The original code removed PKCS#7 padding from the decrypted promo.
        # If the candidate keys are wrong, unpad() can raise ValueError.
        plaintext_with_padding = decrypt_twice(promo, first_number, second_number)
        try:
            plaintext = unpad(plaintext_with_padding, 16)
            print("Decrypted promo:", plaintext.decode("utf-8"))
            return
        except (ValueError, UnicodeDecodeError):
            print("These keys did not produce a valid readable promo. Continue.")

    print("No readable promo was produced. Recheck block alignment/inputs.")


if __name__ == "__main__":
    main()
