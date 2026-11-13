"""[EXTRA] WHAT KIND OF FILE IS THIS?

Files often begin with recognizable bytes (a "magic header").
Use this when a challenge gives you a binary blob, encrypted image,
compressed file, PNG/BMP/PDF, etc.
"""
from pathlib import Path

MAGIC = {b"BM":"BMP picture", b"\x89PNG\r\n\x1a\n":"PNG picture",
         b"%PDF-":"PDF document", b"PK\x03\x04":"ZIP archive",
         b"\x1f\x8b":"GZIP compressed data", b"GIF8":"GIF picture"}


def identify_file(data):
    for prefix, name in MAGIC.items():
        if data.startswith(prefix):
            return name
    return "Unknown file type; not every file has a recognizable header"


def print_hex_view(data, max_bytes=64):
    # 16 bytes per line with the byte offsets to the left.
    for offset in range(0, min(len(data),max_bytes),16):
        chunk=data[offset:offset+16]
        print(f"{offset:04x}: {chunk.hex(' ')}")


if __name__=="__main__":
    sample=b"%PDF-1.7\n..."
    print(identify_file(sample))
    print_hex_view(sample)
    assert identify_file(sample)=="PDF document"
