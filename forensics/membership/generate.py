import struct
import zlib


def create_member(filename: bytes, data: bytes) -> bytes:
    result = b''

    # https://datatracker.ietf.org/doc/html/rfc1952#section-2.3
    result += b'\x1f\x8b' # id
    result += b'\x08' # compression method (deflate)
    result += b'\x08' # flags (bit 3 - FNAME)
    result += b'\x00' * 4 # modification time (0 for now)
    result += b'\x02' # extra flags (2 - maximum compression)
    result += b'\x69' # OS (3 - Unix)

    result += filename + b'\x00' # FNAME

    compress = zlib.compressobj(level=9, method=zlib.DEFLATED, wbits=-zlib.MAX_WBITS, memLevel=zlib.DEF_MEM_LEVEL, strategy=0)
    result += compress.compress(data)
    result += compress.flush()

    checksum = zlib.crc32(data)
    result += struct.pack('<I', checksum) # CRC32
    result += struct.pack('<I', len(data) % 2**32) # ISIZE

    return result


if __name__ == '__main__':
    import os
    import random
    junk_files = [(fname.encode(), open(f'files/{fname}', 'rb')) for fname in os.listdir('files')]
    flag_file = open('flag.png', 'rb')
    result = b''
    result += create_member(b'flag.png', flag_file.read(512))
    files = junk_files + [(b'flag.png', flag_file)]

    while len(files) > 0:
        i = random.randrange(0, len(files))
        name, handle = files[i]
        data = handle.read(random.randint(512, 2048))
        if len(data) == 0:
            handle.close()
            files.pop(i)
        else:
            result += create_member(name, data)
    
    with open('flag.png.gz', 'wb') as f:
        f.write(result)
