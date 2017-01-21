big_A = ord('A')
big_Z = ord('Z')
small_a = ord('a')
small_z = ord('z')

step = 3

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

def encrypt_caesar(plaintext):
    if not plaintext or len(plaintext) == 0:
        return plaintext

    ciphertext = ''
    for i in plaintext:
        ciphertext += shift(i, step)

    return ciphertext

def decrypt_caesar(ciphertext):
    if not ciphertext or len(ciphertext) == 0:
        return ciphertext

    plaintext = ''
    for i in ciphertext:
        plaintext += shift(i, -step)

    return plaintext

def main():
    '''начало программы'''
    print(encrypt_caesar('PYTHON'))
    print(decrypt_caesar('SBWKRQ'))

if __name__ == '__main__':
    main()