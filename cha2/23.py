import os
import random
import Crypto.Cipher.AES as AES
import Crypto.Util.Padding as padding

# 随机密钥与填充
def random_key():
    return os.urandom(16)

def random_padding():
    return os.urandom(random.randint(5, 10))

# 定义函数，随机填充，随机ECB或CBC加密给定的密钥和明文
def encryption_oracle(key, msg):
    mode = random.choice([AES.MODE_ECB, AES.MODE_CBC])
    plaintext = random_padding() + msg + random_padding()
    plaintext = padding.pad(plaintext, 16)
    match mode:
        case AES.MODE_ECB:
            return AES.new(key, mode).encrypt(plaintext), mode
        case AES.MODE_CBC:
            iv = random_key()
            return AES.new(key, mode, iv).encrypt(plaintext), mode
    assert False, "unreachable"

key = random_key()
msg = b"\x00" * 16 * 3  #三个块内容相同
encrypted = [encryption_oracle(key, msg) for _ in range(100)]

def detect_mode(ciphertext):
    blocks = [ciphertext[i : i + 16] for i in range(0, len(ciphertext), 16)]
    if len(blocks) != len(set(blocks)):
        return AES.MODE_ECB
    return AES.MODE_CBC

accr = sum(detect_mode(ciphertext) == mode for ciphertext, mode in encrypted)
print(f"{accr / len(encrypted):.2%}")

#准确率为100.00%