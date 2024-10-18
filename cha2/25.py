import Crypto.Cipher.AES as AES
import Crypto.Util.Padding as padding
 
key = b"\xc6\xfe\xe2/\x97r|/\xeaY\xc5C\xbfi\x99\x97"

def encrypt(userdata: bytes):
    data = (
        b"userdata="
        + userdata.replace(b"&", b"").replace(b"=", b"")
        + b"&uid=10&role=user"
    )
    return AES.new(key, AES.MODE_ECB).encrypt(padding.pad((b"\x00" * 16) + data, 16))
 
 
def decrypt(data: bytes):
    data = AES.new(key, AES.MODE_ECB).decrypt(data)
    data = padding.unpad(data, 16)[16:]
    return {
        (kv := item.split(b"=", maxsplit=1))[0].decode(): kv[1]
        for item in data.split(b"&")
    }
 
 
def is_admin(data: bytes):
    decrypted = decrypt(data)
    print(decrypted)
    return decrypted.get("role") == b"admin"

userdata = b"A" * 7 + b"admin" + b"\x0b" * 14
enc = encrypt(userdata)
enc = enc[:64] + enc[32:48]
assert is_admin(enc)