"""MY FIRST ENIGMA MACHINE — reverse three changing substitution rotors.

WHEN TO TRY: Each typed letter changes rotor positions, so mappings CHANGE.
Rotor 1 advances for each LETTER, rotor 2 after a full rotation of rotor 1,
and rotor 3 after a full rotation of rotor 2.

To DECRYPT, start at rotor 3 (reverse the last substitution),
then rotor 2, then rotor 1. Every call starts with fresh rotors.
"""

ROTOR_1 = "MACHINEBDFGJKLOPQRSTUVWXYZ"
ROTOR_2 = "ORBITACDEFGHJKLMNPQSUVWXYZ"
ROTOR_3 = "CIPHERABDFGJKLMNOQSTUVWXYZ"
CIPHERTEXT = "HKV{BSBU-B-SJYZNNB-DNFW-IXH-YTA-RPL-RTXOLWFQ}"
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def rotate_left(text):
    return text[1:] + text[0]


def decrypt_rotors(ciphertext):
    # Local copies: no global state that survives between multiple runs.
    rotor1 = ROTOR_1
    rotor2 = ROTOR_2
    rotor3 = ROTOR_3
    answer = ""
    letter_count = 0

    for letter in ciphertext:
        if letter not in ALPHABET:
            answer += letter
            continue

        # Rotor 1 advances BEFORE decrypting the current letter.
        rotor1 = rotate_left(rotor1)
        letter_count += 1

        if letter_count % 26 == 0:
            rotor2 = rotate_left(rotor2)
        if letter_count % (26 * 26) == 0:
            rotor3 = rotate_left(rotor3)

        # Backwards through the machine.
        position3 = rotor3.index(letter)
        letter2 = ALPHABET[position3]
        position2 = rotor2.index(letter2)
        letter1 = ALPHABET[position2]
        position1 = rotor1.index(letter1)
        answer += ALPHABET[position1]

    return answer


if __name__ == "__main__":
    print(decrypt_rotors(CIPHERTEXT))
