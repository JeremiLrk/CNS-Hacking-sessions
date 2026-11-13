# ORIGINAL CODE — My First Enigma
# This is your submitted solution. Its program logic is unchanged.
# EXAM TIP: read it top to bottom. Python executes top-level statements immediately.
# Look at solution.py for the reusable, beginner-friendly rewrite.
# Input files for this challenge are in the adjacent data/ folder.

r1 = "MACHINEBDFGJKLOPQRSTUVWXYZ"
r2 = "ORBITACDEFGHJKLMNPQSUVWXYZ"
r3 = "CIPHERABDFGJKLMNOQSTUVWXYZ"

# EXPLAINED: Define a reusable function; its body runs when the function is called.
def Decode(ciphertext):
    global r1, r2, r3
    RESULT = ""
    # EXPLAINED: Repeat the next indented lines for each possible value.
    for char in ciphertext:
        # EXPLAINED: Run the indented block only when this condition is true.
        if char not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            RESULT += char
            continue
        # Rotate rotor 1
        r1 = r1[1:] + r1[0]
        # If rotor 1 completed a full rotation, rotate rotor 2
        if r1 == "MACHINEBDFGJKLOPQRSTUVWXYZ":
            r2 = r2[1:] + r2[0]
            # If rotor 2 completed a full rotation, rotate rotor 3
            if r2 == "ORBITACDEFGHJKLMNPQSUVWXYZ":
                r3 = r3[1:] + r3[0]
        r3_index = r3.index(char)
        r2_char = chr(r3_index + ord("A"))
        r2_index = r2.index(r2_char)
        r1_char = chr(r2_index + ord("A"))
        r1_index = r1.index(r1_char)
        resultchar = chr(r1_index + ord("A"))
        RESULT += resultchar
    print(RESULT)

Decode("HKV{BSBU-B-SJYZNNB-DNFW-IXH-YTA-RPL-RTXOLWFQ}")