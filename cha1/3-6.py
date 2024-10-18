import base64
from idlelib.iomenu import encoding
from binascii import hexlify

def repeatXOR(text, key):
    ciphertext = b''
    i=0
    for e in text:
        a = bytes([e ^ key[i]])
        ciphertext = ciphertext + a
        i = i+1 if i<len(key)-1 else 0
    return ciphertext

def hamming_distance(a, b):
    distance = 0
    for i, j in zip(a, b):
        byte = i ^ j
        distance = distance + sum(k == '1' for k in bin(byte))
    return distance

def English_Scoring(t):
    latter_frequency = {
        'a': .08167, 'b': .01492, 'c': .02782, 'd': .04253,
        'e': .12702, 'f': .02228, 'g': .02015, 'h': .06094,
        'i': .06094, 'j': .00153, 'k': .00772, 'l': .04025,
        'm': .02406, 'n': .06749, 'o': .07507, 'p': .01929,
        'q': .00095, 'r': .05987, 's': .06327, 't': .09056,
        'u': .02758, 'v': .00978, 'w': .02360, 'x': .00150,
        'y': .01974, 'z': .00074, ' ': .15000
    }
    return sum([latter_frequency.get(chr(i), 0) for i in t.lower()])


def ciphertext_XOR(s):
    _data = []
    for single_character in range(256):
        ciphertext = repeatXOR(s, bytes(chr(single_character), encoding='utf-8'))
        score = English_Scoring(ciphertext)
        data = {
            'Single character': single_character,
            'ciphertext': ciphertext,
            'score': score
        }
        _data.append(data)
    score = sorted(_data, key=lambda score: score['score'], reverse=True)[0]
    return score


def Get_the_keysize(ciphertext):
    data = []
    for keysize in range(2, 41):
        block = [ciphertext[i:i + keysize] for i in range(0, len(ciphertext), keysize)]
        distances = []
        for i in range(0, len(block), 2):
            try:
                block1 = block[i]
                block2 = block[i + 1]
                distance = hamming_distance(block1, block2)
                distances.append(distance / keysize)
            except:
                break
        _distance = sum(distances) / len(distances)
        _data = {
            'keysize': keysize,
            'distance': _distance
        }
        data.append(_data)
    _keysize = sorted(data, key=lambda distance: distance['distance'])[0]
    return _keysize


def Break_repeating_key_XOR(ciphertext):
    _keysize = Get_the_keysize(ciphertext)
    keysize = _keysize['keysize']
    print(keysize)
    key = b''
    cipher = b''
    block = [ciphertext[i:i + keysize] for i in range(0, len(ciphertext), keysize)]
    for i in range(0, keysize):
        new_block = []
        t = b''
        for j in range(0, len(block) - 1):
            s = block[j]
            t = t + bytes([s[i]])
        socre = ciphertext_XOR(t)
        key = key + bytes([socre['Single character']])
    for k in range(0, len(block)):
        cipher = cipher + repeatXOR(block[k], key)
    return cipher, key

if __name__ == '__main__':
    with open('6.txt') as of:
        ciphertext = of.read()
        ciphertext = base64.b64decode(ciphertext)
    cipher, key = Break_repeating_key_XOR(ciphertext)
    print("cipher:", cipher, "\nkey:", key)