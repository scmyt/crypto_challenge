import base64
import hashlib
from Crypto.Cipher.AES import new as aes

encoded = "9MgYwmuPrjiecPMx61O6zIuy3MtIXQQ0E59T3xB6u0Gyf1gYs2i3K9Jxaa0zj4gTMazJuApwd6+jdyeI5iGHvhQyDHGVlAuYTgJrbFDrfB22Fpil2NfNnWFBTXyf7SDI"
ciphertext = base64.b64decode(encoded)

def checksum(ks):
    def mapped():
        for i, v in enumerate(ks):
            o = ord(v)
            if 48 <= o <= 57:
                yield i, o - 48
            if 65 <= o <= 90:
                yield i, o - 55
 
    w = [7, 3, 1]
    return sum(k * w[i % len(w)] for i, k in mapped()) % 10
 
 
assert checksum("111116") == 7
 
mrz = "12345678<8<<<1110182<1111167<<<<<<<<<<<<<<<4"

k_seed = hashlib.sha1((mrz[:10] + mrz[13:20] + mrz[21:28]).encode()).digest()[:16]

def gen_key(k_seed, c):
    return bytes(
        ((v & 0b11111110) | ((v & 0b11111110).bit_count() & 1) ^ 1)
        for v in hashlib.sha1(k_seed + bytes([0, 0, 0, c])).digest()[:16]
    )

k = gen_key(k_seed, 1)
ctx = aes(k, 2, b"\x00" * 16)
print(ctx.decrypt(ciphertext))