import itertools
import string

hex_str = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"

cipher_text = bytes.fromhex(hex_str)

def score_english_text(text):
    english_freq = {'e': 12.70, 't': 9.06, 'a': 8.17, 'o': 7.51, 'i': 6.97, 'n': 6.75, 
                    's': 6.33, 'h': 6.09, 'r': 5.99, 'd': 4.25, 'l': 4.03, 'u': 2.76, 
                    'c': 2.78, 'm': 2.41, 'w': 2.36, 'f': 2.23, 'g': 2.02, 'y': 1.97, 
                    'p': 1.93, 'b': 1.29, 'v': 0.98, 'k': 0.77, 'j': 0.15, 'x': 0.15, 
                    'q': 0.10, 'z': 0.07}
    score = 0
    for char in text:
        if char in english_freq:
            score += english_freq[char]
    return score

for key in range(256):
    plain_text = bytes(cipher_text[i] ^ key for i in range(len(cipher_text))).decode('latin1', errors='ignore')
    score = score_english_text(plain_text)
    print(f"Key: {key} Score: {score} Text: {plain_text[:50]}")
