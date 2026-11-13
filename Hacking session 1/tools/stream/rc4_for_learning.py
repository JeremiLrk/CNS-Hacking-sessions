"""[COURSE Part 2] RC4 for UNDERSTANDING the algorithm (not secure today).

RC4 changes an array of 256 values using a secret key. It then produces
one pseudo-random output byte at a time. XOR those output bytes with the
message to encrypt; XOR again to decrypt.

Modern protocols should NOT use RC4. This is for an educational exercise.
"""


def rc4(message, key):
    if not key:
        raise ValueError("Need a key")
    array=list(range(256))
    j=0
    # Key-scheduling algorithm (KSA): mix the array using the key.
    for i in range(256):
        j=(j+array[i]+key[i % len(key)]) % 256
        array[i],array[j]=array[j],array[i]
    # Pseudo-random generation algorithm (PRGA).
    i=j=0
    output=bytearray()
    for byte in message:
        i=(i+1)%256
        j=(j+array[i])%256
        array[i],array[j]=array[j],array[i]
        k=array[(array[i]+array[j])%256]
        output.append(byte ^ k)
    return bytes(output)


if __name__=="__main__":
    encrypted=rc4(b"Plaintext",b"Key")
    print("Known RC4 test vector:",encrypted.hex())
    assert encrypted.hex()=="bbf316e8d940af0ad3"
    assert rc4(encrypted,b"Key")==b"Plaintext"
