def decrypt_single_byte_xor(cipher_hex):
    best_score = -1
    best_key = None
    best_plaintext = None
    english_score = []
    
    # 将十六进制字符串转换为字节串
    cipher_bytes = bytes.fromhex(cipher_hex)
    
    # 尝试从0到255的所有可能的密钥
    for key in range(256):
        # 使用当前密钥进行XOR操作
        plaintext_bytes = bytes(b ^ key for b in cipher_bytes)
        # 将字节串转换为字符串
        plaintext = plaintext_bytes.decode('utf-8', errors='ignore')
        
        # 计算英文字符的评分
        score = sum(english_score[char] for char in plaintext if char in english_score)
        
        # 如果当前评分高于之前最好的评分，更新最佳密钥和明文
        if score > best_score:
            best_score = score
            best_key = key
            best_plaintext = plaintext
    
    return best_key, best_plaintext

# 读取文件中的所有字符串
with open('4.txt', 'r') as file:
    strings = file.readlines()

# 对每个字符串进行检测
for s in strings:
    cipher_hex = s.strip()
    key, plaintext = decrypt_single_byte_xor(cipher_hex)
    if key is not None and plaintext is not None:
        print(f"Found XORed string: {plaintext} with key: {key}")