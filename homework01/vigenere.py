big_A = ord('A')
big_Z = ord('Z')
small_a = ord('a')
small_z = ord('z')

def _get_shift_size(long_keyword, position):
    c = long_keyword[position]
    return ord(c) - (big_A if c.istitle() else small_a)


def _get_long_keyword(keyword, required):
    long_keyword = keyword
    while len(long_keyword) < required:
        long_keyword += keyword

    return long_keyword[0:required]

def shift(c, shift_size):
    return _shift(c, shift_size,
                  big_A if c.istitle() else small_a,
                  big_Z if c.istitle() else small_z)

def _shift(c, shift_size, left_border, right_border):
    code = ord(c)
    if (code >= (right_border - shift_size)) and (code <= right_border):
        code = code - (right_border - left_border) + shift_size - 1
    elif code < (left_border + 3):
        code = code + (right_border - left_border) + shift_size + 1
    elif ((code >= left_border) and (code <= (right_border - shift_size))):
        code = code + shift_size

    return chr(code)



def encrypt_vigenere(plaintext, keyword):
    if not plaintext or len(plaintext) == 0 or not keyword or len(keyword) == 0:
        return plaintext

    long_keyword = _get_long_keyword(keyword, len(plaintext))

    ciphertext = ''
    for i in range(0, len(plaintext)):
        ciphertext += shift(plaintext[i], _get_shift_size(long_keyword, i))

    return ciphertext

def decrypt_vigenere(ciphertext, keyword):
    if not ciphertext or len(ciphertext) == 0 or not keyword or len(keyword) == 0:
        return ciphertext

    long_keyword = _get_long_keyword(keyword, len(ciphertext))

    plaintext = ''
    for i in range(0, len(ciphertext)):
        plaintext += shift(ciphertext[i], -_get_shift_size(long_keyword, i))

    return plaintext

def main():
    '''начало программы'''
    print(encrypt_vigenere("PYTHON", "A"))
    print(decrypt_vigenere("python", "a"))
    print(encrypt_vigenere("LXFOPVEFRNHR", "LEMON"))

if __name__ == '__main__':
    main()