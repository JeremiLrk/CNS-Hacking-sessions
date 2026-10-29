"""BETTER HASH — reverse a function that is NOT a true one-way hash.

WHEN TO TRY: You see a 'hash' that preserves message length and only uses
reversible operations (XOR, bit rotations, array rotation).

Undo operations in REVERSE order:
  original round: XOR constant -> rotate byte left -> prefix XOR -> rotate array
  reversed:       rotate array back -> undo prefix XOR -> rotate right -> XOR

A real cryptographic hash intentionally loses information and is not
normally invertible in this way.
"""

TARGET_HASH = "5f070b54361613bca31a123e95321cff154ba64f549bb34fdc7688f10efb569aed4ccbd6ba"


def rotate_left_8(value, count):
    count %= 8
    return ((value << count) | (value >> (8 - count))) & 255


def rotate_right_8(value, count):
    count %= 8
    return ((value >> count) | (value << (8 - count))) & 255


def better_hash(message):
    data = bytearray(message.encode())
    for round_number in range(8):
        for index in range(len(data)):
            data[index] ^= (round_number * 41 + index * 17) & 255
            data[index] = rotate_left_8(data[index], (round_number + index) & 7)

        for index in range(1, len(data)):
            data[index] ^= data[index - 1]

        data = data[1:] + data[:1]

    return data.hex()


def reverse_better_hash(hash_hex):
    data = bytearray.fromhex(hash_hex)

    for round_number in reversed(range(8)):
        # The last step was rotate array LEFT by 1. Undo with RIGHT by 1.
        data = data[-1:] + data[:-1]

        # Undo prefix XOR in REVERSE index order. Example:
        # after[i] = before[i] XOR after[i-1].
        for index in reversed(range(1, len(data))):
            data[index] ^= data[index - 1]

        # Undo byte left rotation and finally undo XOR with constant.
        for index in reversed(range(len(data))):
            shift = (round_number + index) & 7
            data[index] = rotate_right_8(data[index], shift)
            data[index] ^= (round_number * 41 + index * 17) & 255

    return data.decode("utf-8")


if __name__ == "__main__":
    answer = reverse_better_hash(TARGET_HASH)
    print("Recovered message:", answer)
    assert better_hash(answer) == TARGET_HASH
    print("Verified by hashing the recovered message again.")
