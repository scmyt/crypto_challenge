def fixed_xor(hex_str1, hex_str2):

    b1 = bytes.fromhex(hex_str1)
    b2 = bytes.fromhex(hex_str2)
    
    xor_result = bytes(a ^ b for a, b in zip(b1, b2))
    return xor_result.hex()

hex_str1 = "1c0111001f010100061a024b53535009181c"
hex_str2 = "686974207468652062756c6c277320657965"

result = fixed_xor(hex_str1, hex_str2)
print(result)