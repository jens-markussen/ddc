import socket
import time

HOST = "diskenc.cfire"
PORT = 1337

# In XTS mode, tweak MUST match block position in file.
# Oracle block 0 (tweak=0) → can only forge file block 0
# Oracle block 1 (tweak=1) → can only forge file block 1
#
# "administrator:x:" = exactly 16 bytes → perfect block boundary!
# So if administrator entry starts at block 0:
#   block 0 = "administrator:x:"  (username, can't change)
#   block 1 = "0:0::/home/admin"  (uid/gid, we forge with tweak=1)

def make_oracle_input(plain0: str, plain1: str) -> str:
    b0 = plain0.encode().ljust(16, b'\x00').hex()
    b1 = plain1.encode().ljust(16, b'\x00').hex()
    return f"{b0} {b1}"

def read_until(sock, marker, timeout=5):
    sock.settimeout(timeout)
    data = b""
    try:
        while marker.encode() not in data:
            data += sock.recv(4096)
    except socket.timeout:
        pass
    return data.decode(errors="replace")

def try_forge(oracle_input, restore_block, use_ct_index, label):
    """
    oracle_input:  two hex blocks for the oracle
    restore_block: which block number in passwd file to overwrite
    use_ct_index:  0 or 1 — which oracle CT to use (MUST equal restore_block for XTS to work)
    """
    print(f"\n[*] {label}")
    print(f"    restore_block={restore_block}, CT[{use_ct_index}]")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))

        read_until(s, "ECB.")
        print(f"    Connected.")

        s.sendall((oracle_input + "\n").encode())
        time.sleep(0.5)

        response = read_until(s, "contents")
        print(f"    Oracle response: {response.strip()}")

        # Parse both ciphertext blocks
        ct_line = None
        for line in [l.strip() for l in response.splitlines() if l.strip()]:
            parts = line.split()
            if len(parts) == 2 and all(c in '0123456789abcdef' for c in parts[0]+parts[1]):
                ct_line = parts
                break

        if not ct_line:
            print(f"    Could not parse ciphertext!")
            s.close()
            return False

        ct = ct_line[use_ct_index]
        print(f"    Using CT: {ct}")

        s.sendall(f"{restore_block} {ct}\n".encode())
        time.sleep(0.5)

        result = read_until(s, "\n", timeout=3)
        print(f"    Result: {result.strip()}")
        s.close()

        if "ERROR" not in result and "Unauthorized" not in result:
            print(f"\n[!!!] SUCCESS!")
            return True

    except Exception as e:
        print(f"    Exception: {e}")

    return False

attempts = [
    # The ONLY valid attacks: CT[N] → file block N (XTS tweak constraint)
    # Attempt 1: administrator is first entry (block 0), uid field is block 1
    {
        "oracle_input": make_oracle_input("administrator:x:", "0:0::/home/admin"),
        "restore_block": 1,
        "use_ct_index": 1,
        "label": "admin at block 0 → forge uid field at block 1"
    },
    # Attempt 2: maybe password field is empty not x
    {
        "oracle_input": make_oracle_input("administrator::", "0:0::/home/admin"),
        "restore_block": 1,
        "use_ct_index": 1,
        "label": "admin at block 0 (no shadow) → forge uid field at block 1"
    },
    # Attempt 3: try restoring block 0 with identical content to test if restore works at all
    {
        "oracle_input": make_oracle_input("administrator:x:", "0:0::/home/admin"),
        "restore_block": 0,
        "use_ct_index": 0,
        "label": "restore block 0 with same username (sanity check)"
    },
]

for attempt in attempts:
    success = try_forge(**attempt)
    if success:
        print("\n[+] Try: su - administrator (blank password)")
        break
    time.sleep(2)

print("\n[*] Done.")