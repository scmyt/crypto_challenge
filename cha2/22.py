import base64
from aes import context as aes_context

def strxor(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))

def cbc_encrypt(
    blocks: list[bytes], iv: bytes, transform: Callable[[bytes], bytes]
) -> list[bytes]:
    result = [iv]
    for block in blocks:
        result.append(transform(strxor(block, result[-1])))
    return result

def cbc_decrypt(
    blocks: list[bytes], iv: bytes, transform: Callable[[bytes], bytes]
) -> list[bytes]:
    result = [strxor(transform(blocks[0]), iv)]
    for index, block in enumerate(blocks[1:]):
        result.append(strxor(transform(block), blocks[index]))
    return result

def split_blocks(message, block_size=16):
    assert len(message) % block_size == 0
    return [message[i:i+16] for i in range(0, len(message), block_size)]

ciphertext = base64.b64decode("""
/* here is ciphertext */
""")
key = b"YELLOW SUBMARINE"
ctx = aes_context(key)
 
print(b"".join(cbc_decrypt(split_blocks(ciphertext), b"\x00"*16, ctx.decrypt_block)))