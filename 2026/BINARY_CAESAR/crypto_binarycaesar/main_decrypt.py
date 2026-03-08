import string
import random

alphabet = 'abcdefghijklmnopqrstuvwxyzæøå{}_'

# Rotate each character by the index of the key character
def xor(a, b):
    # Ignore spaces
    if a in string.whitespace:
        return a
    return alphabet[(alphabet.index(a) ^ alphabet.index(b))]

def caesar_encrypt(key, text):
    ciphertext = ""
    for i in range(len(text)):
        ciphertext += xor(text[i], key)
    return ciphertext

def main():
    # Danish text, flag is in text
    with open('encryption.txt', 'rb') as f:
        ciphertext = f.read().decode("utf-8").strip()

    for key in alphabet:
        text = caesar_encrypt(key, ciphertext)

        print(f'Key: {key}, text: {text}')
        if 'ddc' in text:
            print(f'YES YES YES')

    
    # Once you have decrypted the ciphertext, remember to add flag formatting
    # For example:
    # ddc example flag
    # to
    # ddc{example_flag}


if __name__ == '__main__':
    main()
