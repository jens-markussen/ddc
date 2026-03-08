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

key = 'a'
while (key == 'a'):
	key = random.choice(alphabet)

def main():
    # Danish text, flag is in text
    with open('flag.txt', 'rb') as f:
        text = f.read().decode("utf-8").strip()

    ciphertext = caesar_encrypt(key, text)

    with open('encryption.txt', 'wb') as f:
        f.write(ciphertext.encode("utf-8"))

    # Once you have decrypted the ciphertext, remember to add flag formatting
    # For example:
    # ddc example flag
    # to
    # ddc{example_flag}


if __name__ == '__main__':
    main()
