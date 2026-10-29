# ORIGINAL CODE — Noncense
# This is your submitted solution. Its program logic is unchanged.
# EXAM TIP: read it top to bottom. Python executes top-level statements immediately.
# Look at solution.py for the reusable, beginner-friendly rewrite.
# Input files for this challenge are in the adjacent data/ folder.

# EXPLAINED: Import a Python library so this script can use its functions.
from Crypto.Cipher import AES
from Crypto.Util import Counter

# EXPLAINED: Define a reusable function; its body runs when the function is called.
def encrypt(key, nonce, msg):
    ctr = Counter.new(64, prefix=nonce)
    # EXPLAINED: Create the AES cipher with the specified key and mode.
    cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
    return cipher.encrypt(msg)


def retrieve_keystream(plaintext, ciphertext):
    # EXPLAINED: Pair items from two inputs. zip() stops at the shorter input.
    keystream = bytes(a ^ b for a, b in zip(plaintext, ciphertext))
    return keystream


def decrypt_with_retrieved_keystream(ciphertext, keystream):
    answer = bytes(a ^ b for a, b in zip(ciphertext, keystream))
    return answer


plaintext = ("According to all known laws of aviation, there is no way a bee should be able to fly.").encode()

# EXPLAINED: Turn printable hexadecimal digits into the real bytes they describe.
ciphertext1 = bytes.fromhex("fcf83b2f47f34aa6f48d09c87b65a558c5290cec3fd64a2a06c8d687c02bfa5e5fd512cc4854686920f59867edc05aaf9a21560e359928e343cdd4b6ea3ce69267e267a51b2b25522a83d210ca3fc89a684f399e6a")

ciphertext2 = bytes.fromhex("def52b3b54f25097f0d90ff8356ba757801d10e63dcb0f190eccfac3ce23bd5a5bd306cb5c")
keystream = retrieve_keystream(plaintext, ciphertext1)
answer = decrypt_with_retrieved_keystream(ciphertext2, keystream)
print(answer)
