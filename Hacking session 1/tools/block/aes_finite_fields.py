"""[COURSE Part 2] AES MATH: GF(2^8) (finite fields).

You don't multiply bytes normally inside AES MixColumns.
Think of each byte as an 8-bit polynomial. You combine them with XOR and
reduce over the special polynomial x^8+x^4+x^3+x+1 (hex 0x11B).

WHEN TO USE:
- Exercise mentions MixColumns, finite fields, polynomial multiplication.
- You see `xtime`, `0x1b`, or multiplication by 2 and 3.
"""


def gf_multiply(first, second):
    answer = 0
    for _ in range(8):
        if second & 1:
            answer ^= first
        went_over_255 = first & 0x80
        first = (first << 1) & 0xff
        if went_over_255:
            first ^= 0x1b
        second >>= 1
    return answer


def mix_one_aes_column(col):
    if len(col) != 4:
        raise ValueError("AES column must be exactly four bytes")
    a, b, c, d = col
    return bytes([
        gf_multiply(a,2) ^ gf_multiply(b,3) ^ c ^ d,
        a ^ gf_multiply(b,2) ^ gf_multiply(c,3) ^ d,
        a ^ b ^ gf_multiply(c,2) ^ gf_multiply(d,3),
        gf_multiply(a,3) ^ b ^ c ^ gf_multiply(d,2),
    ])


if __name__ == "__main__":
    print("AES test 0x57 * 0x83 =", hex(gf_multiply(0x57, 0x83)))
    assert gf_multiply(0x57, 0x83) == 0xC1
