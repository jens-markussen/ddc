import hashlib


# BB707DD63F792BFA73AD00C993875811

words = ['“Denne gang er hasheren fuldstændig umulig at knække.”']

for w in words:
    print(w, hashlib.md5(w.encode()).hexdigest())