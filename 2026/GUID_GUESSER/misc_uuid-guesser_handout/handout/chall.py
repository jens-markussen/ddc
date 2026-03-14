#!/usr/bin/env python3

import hashlib
import random
import time
import uuid

# we seed the random with random :D gl
random.seed(random.getrandbits(64))

NEEDED_SUCCESSES = 5
MAX_ATTEMPTS = NEEDED_SUCCESSES * 3
PEPPER = random.getrandbits(64).to_bytes(8)

def generate_uuid(version: int) -> uuid.UUID:
    if version == 1: ##
        return uuid.uuid1(node=random.getrandbits(48))
    if version == 2:
        # Python's stdlib doesn't expose UUIDv2 :c
        raise NotImplementedError("UUIDv2 is not supported by Python's standard library")
    if version == 3: ##
        return uuid.uuid3(uuid.NAMESPACE_DNS, str(random.getrandbits(2026)))
    if version == 4:
        return uuid.uuid4()
    if version == 5: ##
        return uuid.uuid5(uuid.NAMESPACE_DNS, str(random.getrandbits(2026)))
    if version == 6: ##
        return uuid.uuid6(node=random.getrandbits(48))
    if version == 7:
        return uuid.uuid7()
    if version == 8: ##
        return uuid.uuid8()
    raise ValueError("Version must be an integer between 1 and 8")

def main() -> None:
    attempts_left = MAX_ATTEMPTS
    locked: set[int] = set()

    print(
        "---------------------------------------------------\n"
        f" Welcome to the UUID Guesser!\n"
        " - Choose a UUID version (1-8)\n"
        f" - You have {MAX_ATTEMPTS} total attempts\n"
        f" - Solve {NEEDED_SUCCESSES} different UUIDs to get the flag\n"
        "---------------------------------------------------\n"
    )

    while attempts_left > 0 and len(locked) < NEEDED_SUCCESSES:
        print(f"Solved: {len(locked)}/{NEEDED_SUCCESSES} | Remaining attempts: {attempts_left}")

        try:
            version = int(input("Version (1-8): ").strip())
        except Exception as e:
            return
        if not (1 <= version <= 8):
            print("Please enter a number from 1 to 8.\n")
            continue
        if version in locked:
            print("You've already correctly guessed this version. Try another one.\n")
            continue

        try:
            count = int(input("How many UUIDs to generate before guessing?: ").strip())
        except Exception as e:
            return
        if count < 1 or count > 10:
            print("Please enter a number between 1 and 10.\n")
            continue

        bank = set()
        for i in range(count):
            target = generate_uuid(version)
            SALT = random.getrandbits(32).to_bytes(4)
            hint = target.bytes[:4].hex() 
            print(f"[{i+1}] UUIDv{version} hint: {hint}...@sha256:{hashlib.sha256(target.bytes + SALT + PEPPER).hexdigest()}")
            bank.add(target)

        attempts_left -= 1
        try:
            guess = input("Your guess: ").strip()
            guess_uuid = uuid.UUID(guess)
        except Exception as e:
            print("Invalid UUID format. Try again.\n")
            continue

        if guess_uuid in bank:
            locked.add(version)
            print(f"Correct! ({len(locked)}/{NEEDED_SUCCESSES})\n")
        else:
            print(f"Wrong. It was: {target} with salt {SALT.hex()}\n")

    if len(locked) >= NEEDED_SUCCESSES:
        with open("flag.txt", "r") as f:
            flag = f.read().strip()
            print("Congratulations! You've correctly guessed enough UUID versions.")
            print(f"Here is your flag: {flag}")
    else:
        print("Out of guesses! Better luck next time.")

if __name__ == "__main__":
    main()
