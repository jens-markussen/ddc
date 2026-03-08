import string
import random
import math

alphabet = 'abcdefghijklmnopqrstuvwxyz'

phi = (1 + math.sqrt(5)) / 2
psi = (1 - math.sqrt(5)) / 2
sqrt5 = math.sqrt(5)

def fib_closed(n):
    """
    Compute F_n using the closed-form expression.
    Valid for moderate n (educational use).
    """
    return int(round((pow(phi, n, len(alphabet)) - pow(psi, n, len(alphabet))) / sqrt5))

def fib(n, mod):
    def _fib(k):
        if k == 0:
            return (0, 1)
        a, b = _fib(k >> 1)
        c = (a * ((b << 1) - a)) % mod
        d = (a * a + b * b) % mod
        if k & 1:
            return (d, (c + d) % mod)
        else:
            return (c, d)
    return _fib(n)[0]

def fib_caesar_encrypt(n, text):
    a = fib(n, len(alphabet))
    b = fib(n + 1, len(alphabet))
    out = []
    for c in text:
        if c in string.whitespace:
            out.append(c)
            continue
        k = a % len(alphabet)
        a, b = b, a + b
        out.append(alphabet[(alphabet.index(c) + k) % len(alphabet)])
    return "".join(out)

key = random.randint(0, 2**128)

def main():
    # Danish text, flag is in text
    with open('flag.txt', 'rb') as f:
        text = f.read().decode("utf-8").strip()

    ciphertext = fib_caesar_encrypt(key, text)
    print(ciphertext)

    with open('encryption.txt', 'wb') as f:
        f.write(ciphertext.encode("utf-8"))

    # Once you have decrypted the ciphertext, remember to add flag formatting
    # For example:
    # ddc example flag
    # to
    # ddc{example_flag}

if __name__ == '__main__':
    main()
