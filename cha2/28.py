import Crypto.Cipher.AES as AES
import Crypto.Util.Padding as padding
import os
 
key = b"\xc6\xfe\xe2/\x97r|/\xeaY\xc5C\xbfi\x99\x97"

def encrypt(userdata: bytes):
    data = (
        b"comment1=cooking MCs;userdata="
        + userdata.replace(b";", b"%3B").replace(b"=", b"%3D")
        + b";comment2= like a pound of bacon"
    )
    return AES.new(key, AES.MODE_CBC, os.urandom(16)).encrypt(
        padding.pad((b"\x00" * 16) + data, 16)
    )

def decrypt(data: bytes):
    data = padding.unpad(AES.new(key, AES.MODE_CBC, os.urandom(16)).decrypt(data), 16)[
        16:
    ]
    return {
        (kv := item.split(b"=", maxsplit=1))[0].decode(): kv[1]
        for item in data.split(b";")
    }

def is_admin(data: bytes):
    decrypted = decrypt(data)
    return decrypted.get("admin") == b"true"

padlen = 18
userdata = b"A" * padlen + b":admin<true"
enc = bytearray(encrypt(userdata))
enc[padlen + 30] ^= 1
enc[padlen + 36] ^= 1
assert is_admin(enc)