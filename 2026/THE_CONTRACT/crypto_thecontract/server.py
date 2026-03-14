#!/usr/bin/python
import hashlib
import sys

APPROVED_SHA1 = "7119d27d6ede2334872c949e68f13ad3680de5bf"
CACHED_MD5 = "7ba2f771fa259883b53a081081d37998"

def md5(data: bytes) -> str:
    return hashlib.md5(data).hexdigest()

def sha1(data: bytes) -> str:
    return hashlib.sha1(data).hexdigest()

def verify_contract(data: bytes):
    # Ignore the appendix
    appendix_str = b"------- BEGIN APPENDIX A -------"
    appendix_idx = data.index(appendix_str)

    h1 = sha1(data[:appendix_idx+len(appendix_str)])
    if h1 != APPROVED_SHA1:
        return False, "Hash mismatch"

    h2 = md5(data[:appendix_idx+len(appendix_str)])
    if h2 == CACHED_MD5:
        return False, "⚠️ Cannot update with same contract"

    text = data.decode("utf-8", errors="ignore")

    # Contract header must approve
    if "Decision: APPROVE" not in text:
        return False, "Contract not approved"

    if "ASSETS ARE TRANSFERRED NOW" in text:
        with open("flag.txt", mode='r') as file: # b is important -> binary
            return True, file.read()

    return True, "✅ Contract accepted"

print("Welcome to the contract updating system.\n\nPlease sumit your contract:", end="\n")

sys.stdout.flush()
data = sys.stdin.buffer.read(512)

ok, msg = verify_contract(data)
print(msg)
assert(ok)

