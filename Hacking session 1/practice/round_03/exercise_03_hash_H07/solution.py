"""H07: find any collision in the FIRST THREE BYTES of SHA-256.

A collision needs two DIFFERENT inputs with the same hash prefix.
Since 3 bytes = 24 bits, a birthday attack often needs only ~2^12 trials.
This is NOT reversing SHA-256: truncation makes the search easy.
"""
import hashlib

def main():
    visited={}
    attempt=0
    while True:
        # Every counter value gives a different short message.
        message=attempt.to_bytes(8,'big')
        short_hash=hashlib.sha256(message).digest()[:3]
        if short_hash in visited:
            older=visited[short_hash]
            if older != message:
                print('Both share truncated digest:',short_hash.hex())
                print('SUBMIT:',older.hex()+':'+message.hex())
                return
        else:
            visited[short_hash]=message
        attempt += 1

if __name__=='__main__':
    main()
