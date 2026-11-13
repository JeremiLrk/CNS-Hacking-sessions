# ORIGINAL CODE — Security Cam
# This is your submitted solution. Its program logic is unchanged.
# EXAM TIP: read it top to bottom. Python executes top-level statements immediately.
# Look at solution.py for the reusable, beginner-friendly rewrite.
# Input files for this challenge are in the adjacent data/ folder.

# EXPLAINED: Import a Python library so this script can use its functions.
import hashlib

username = "user"
realm = "PythonRTSP"
method = "DESCRIBE"
uri = "rtsp://cns-test.idlab.uantwerpen.be:50002/video"
nonce = "4874a055c3f4390506d99e6c51a9e3e360cbef8a62abd7079e11faddcb70a38c"
target_response = "b3539154c5b784bba2c47a1a6c7c4ab0"
data2 = f"{method}:{uri}"
# EXPLAINED: Convert ordinary text into bytes before performing byte operations.
ha2 = hashlib.md5(data2.encode()).hexdigest()

count = 0

with open("rockyou.txt", "rb") as passwords:
    # EXPLAINED: Repeat the next indented lines for each possible value.
    for password in passwords:
        count += 1
        dapassword = password.rstrip(b"\r\n")
        data = f"{username}:{realm}:".encode() + dapassword
        # EXPLAINED: Calculate a cryptographic digest of the bytes supplied here.
        ha1 = hashlib.md5(data).hexdigest()
        data3 = f"{ha1}:{nonce}:{ha2}"
        response = hashlib.md5(data3.encode()).hexdigest()
        # EXPLAINED: Run the indented block only when this condition is true.
        if response == target_response:
            print(password)
            break
        # Show progress every 100,000 passwords
        if count % 100000 == 0:
            print(f"Tested {count:,} passwords...")