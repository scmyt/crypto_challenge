import os
import Crypto.Cipher.AES as AES
import Crypto.Util.Padding as padding
import base64
import string

#先对明文加密
def encryption_oracle(oracle):
    key = os.urandom(16)
    return AES.new(key, AES.MODE_ECB).encrypt(
        padding.pad(
            oracle
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

plain_space = string.printable.encode()

# dfs搜索明文
def search(known):
    while True:
        partial = known[-15:] # 取明文的最后15字节（可能不足）
        partial = b"\x00" * (15 - len(partial)) + partial # 补齐到15字节
        current = []
        for i in plain_space:
            oracle = partial + bytes([i]) + b"\x00" * (15 - len(known) % 16) # 构造 oracle，让第一个未知明文在块的最后一个字节
            enc = encryption_oracle(oracle)
            if enc[15] == enc[len(known) // 16 * 16 + 31]: # 成功碰撞
                current.append(i)
        if len(current) == 1:
            known += bytes(current) # 不递归，用循环，防止爆栈
            print(known)
            if len(known) == unk_strlen: # 达到预期长度，成功退出
                return True
            continue
        elif len(current) == 0: # 没有成功碰撞，失败退出
            return False
        else:
            for c in current: # 对每一个碰撞
                if search(known + bytes([c])): # 递归搜索
                    return True # 找到结果就返回

search(b'')