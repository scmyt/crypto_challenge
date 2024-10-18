def repeating_key_xor(plaintext, key):
    # 将文本和密钥都转换为字节
    plaintext_bytes = bytes(plaintext, 'utf-8')
    key_bytes = bytes(key, 'utf-8')
    
    # 初始化一个空的字节数组来存储结果
    result = bytearray()
    
    # 初始化一个密钥索引
    key_index = 0
    
    # 对每个明文字符进行XOR操作
    for byte in plaintext_bytes:
        # 将密钥的当前字节与明文字节XOR，并将结果添加到结果数组中
        result.append(byte ^ key_bytes[key_index])
        
        # 更新密钥索引，如果到达密钥末尾则重置
        key_index = (key_index + 1) % len(key_bytes)
    
    # 将结果转换为十六进制字符串
    return result.hex()

# 给定的明文和密钥
plaintext = "Burning 'em, if you ain't quick and nimble I go crazy when I hear a cymbal"
key = "ICE"

# 调用函数并打印结果
encrypted_text = repeating_key_xor(plaintext, key)
print(encrypted_text)