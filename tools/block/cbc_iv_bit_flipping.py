"""[COURSE Part 2 + EXTRA] CBC IV BIT FLIP (only first block).

In CBC mode, the first plaintext block is:
    P1 = AES_DECRYPT(C1) XOR IV

Changing the IV changes the first decrypted block, even without the key.
But if the ciphertext is protected by a MAC or AEAD, the server should
REJECT the modified data. This works ONLY with unprotected CBC.
"""


def change_first_cbc_block_iv(iv, old_first_plain_block, new_first_plain_block):
    if len(iv)!=16 or len(old_first_plain_block)!=16 or len(new_first_plain_block)!=16:
        raise ValueError("Every input must be exactly 16 bytes")
    answer=bytearray()
    for iv_byte,old_byte,new_byte in zip(iv,old_first_plain_block,new_first_plain_block):
        answer.append(iv_byte ^ old_byte ^ new_byte)
    return bytes(answer)


if __name__=="__main__":
    iv=bytes(range(16))
    old=b"0000000000000000"
    new=b"1111111111111111"
    new_iv=change_first_cbc_block_iv(iv,old,new)
    print("Modified IV:",new_iv.hex())
    assert bytes(a^b^c for a,b,c in zip(iv,old,new))==new_iv
