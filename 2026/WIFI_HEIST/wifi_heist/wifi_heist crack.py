#!/usr/bin/env python3

# ================================================================
#
#        _  _  _ _____ _______ _____
#       | || || (_____(_______|_____)
#       | || || |_   _ _____     _
#       | ||_|| | | | |  ___)   | |
#       | |___| |_| |_| |     __| |__
#        \______|_____|_|    |______)
#
#       H   E   I   S   T       v1.0
#
# ================================================================
#
#   THE STORY:
#   ----------
#   The IT guy at school just changed the WiFi password.
#   Again. For the 4th time this month.
#
#   Nobody knows the new password, the printer queue is
#   dead, and people are burning through their mobile data
#   watching TikToks in the cafeteria.
#
#   BUT... your friend found this Python script on a USB
#   stick the IT guy left behind. It's the script he uses
#   to scramble the WiFi password before storing it.
#
#   You also found the scrambled password he saved
#   (see 'scrambled_password' below).
#
#   YOUR MISSION:
#   Reverse the scramble. Get the password. Be the hero.
#   The flag is in the format DDC{...}
#
#   HINT: The IT guy did 3 steps to hide the password.
#   Just UNDO each step... in REVERSE order!
#   (undo step 3 first, then step 2, then step 1)
#
#   You got this.
#
# ================================================================


def it_guy_scramble(password):
    """This is how the IT guy hides the WiFi password."""

    # STEP 1: Shift every character forward by 3
    # (each letter becomes the letter 3 places ahead)
    shifted = []
    for char in password:
        shifted.append(chr(ord(char) + 3))

    # STEP 2: Flip the whole thing backwards
    backwards = shifted[::-1]

    # STEP 3: Mix each character with the IT guy's
    # favorite number (42) using XOR
    magic_number = 42
    mixed = []
    for char in backwards:
        mixed.append(ord(char) ^ magic_number)

    return mixed


# ============================================================
#  THIS is the scrambled password found on the USB stick!
#  Reverse the steps above to decode it.
# ============================================================

scrambled_password = [
    170,
    28,
    77,
    25,
    76,
    72,
    28,
    65,
    93,
    72,
    77,
    28,
    68,
    76,
    29,
    95,
    76,
    72,
    82,
    25,
    86,
    84,
    108,
    109,
    109,
]


# Plug in your answer here to see if you cracked it!
def check_flag(your_answer):
    if it_guy_scramble(your_answer) == scrambled_password:
        print()
        print("  =============================================")
        print("    WiFi password CRACKED!")
        print(f"    The flag is: {your_answer}")
        print()
        print("    You just reversed your first cipher!")
        print("    Now go share the WiFi with the boys.")
        print("  =============================================")
        print()
    else:
        print()
        print("  Nope, that's not it. Keep going!")
        print("  Remember: UNDO step 3, then step 2, then step 1.")
        print()


# ============================================================
#  YOUR SOLVE SCRIPT GOES HERE!
#
#  Think about it:
#    - The LAST thing the IT guy did was Step 3 (XOR).
#      So the FIRST thing you undo is... the XOR!
#    - Then undo Step 2 (the reversal)
#    - Then undo Step 1 (the shift)
#
#  Useful Python reminders:
#    chr(number)  -> gives you a character
#    ord(char)    -> gives you a number
#    a ^ b        -> XOR operation
#    list[::-1]   -> reverses a list
#
#  Uncomment and fill in the line below when you have the flag:
# check_flag("DDC{???}")
# ============================================================


def unscramble(scrambled_password):
    """This is how the IT guy hides the WiFi password."""

    # STEP 3: Mix each character with the IT guy's
    # favorite number (42) using XOR
    # REVERSE IS THE SAME
    magic_number = 42
    unmagic = []
    for char in scrambled_password:
        unmagic.append(char ^ magic_number)

    # STEP 2: Flip the whole thing backwards
    # REVERSE IS THE SAME
    backwards = unmagic[::-1]

    # STEP 1: Shift every character forward by 3
    # (each letter becomes the letter 3 places ahead)
    # REVERSE IS 3 LETTERS BACK
    # password = []
    password = ""
    for char in backwards:
        password += chr(char - 3)

    return password

password = unscramble(scrambled_password)

print(password)

print(check_flag(password))