import os
import Crypto.Cipher.AES as AES
import Crypto.Util.Padding as padding
import base64
import string
import random

PREFIX_LENGTH = random.randint(0, 64)

def encryption_oracle(oracle):
    key = os.urandom(16)
    rand_pad = os.urandom(PREFIX_LENGTH)
    return AES.new(key, AES.MODE_ECB).encrypt(
        padding.pad(
            rand_pad
            + oracle
            + base64.b64decode("""
Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg
aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq
dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg
YnkK"""),
            16,
        )
    )

# 爆破明文长度
init_unk_strlen = len(encryption_oracle(b""))
unk_strlen = init_unk_strlen
assert unk_strlen % 16 == 0
for i in range(16):
    if len(encryption_oracle(b"A" * i)) != init_unk_strlen:
        unk_strlen = init_unk_strlen - i
        break

#求前缀长度
def get_unklen():
    init_unk_strlen = len(encryption_oracle(b""))
    unk_strlen = init_unk_strlen
    assert unk_strlen % 16 == 0
    for i in range(16):
        if len(encryption_oracle(b"A" * i)) != init_unk_strlen:
            unk_strlen = init_unk_strlen - i
            break
    leftlen = 0
    while True:
        leftlen += 1
        enc = encryption_oracle(b"A" * leftlen)
        blocks = [enc[i : i + 16] for i in range(0, len(enc), 16)]
        for i in range(len(blocks) - 1):
            if blocks[i] == blocks[i + 1]:
                return unk_strlen - i * 16 + leftlen % 16, i * 16, leftlen % 16
 
 
unk_strlen, offset, leftpad = get_unklen()
leftpad = b"\x00" * leftpad

plain_space = string.printable.encode()

#补全并丢弃
def search(known):
    while True:
        partial = known[-15:]
        partial = b"\x00" * (15 - len(partial)) + partial
        current = []
        for i in plain_space:
            oracle = leftpad + partial + bytes([i]) + b"\x00" * (15 - len(known) % 16)
            enc = encryption_oracle(oracle)[offset:]
            if enc[15] == enc[len(known) // 16 * 16 + 31]:
                current.append(i)
        if len(current) == 1:
            known += bytes(current)
            print(known)
            if len(known) == unk_strlen:
                return True
            continue
        elif len(current) == 0:
            return False
        else:
            for c in current:
                if search(known + bytes([c])):
                    return True

search(b"")