#!/usr/bin/env python3

import argparse

import hashlib

import random

import re

import socket

import sys

import time

import uuid

from typing import Dict, Iterable, List, Optional, Sequence, Tuple

 

UUID_EPOCH_100NS = 0x01B21DD213814000

WRONG_GUESS = "00000000-0000-0000-0000-000000000000"

FLAG_V6 = (6 << 76) | (0b10 << 62)

FLAG_V8 = (8 << 76) | (0b10 << 62)

 

 

class Tube:

    def __init__(self, host: str, port: int, timeout: float = 10.0) -> None:

        self.sock = socket.create_connection((host, port), timeout=timeout)

        self.sock.settimeout(timeout)

        self.buf = b""

        self.at_version_prompt = False

 

    def close(self) -> None:

        try:

            self.sock.close()

        except OSError:

            pass

 

    def sendline(self, s: str) -> None:

        self.sock.sendall(s.encode() + b"\n")

 

    def recv_until_any(self, markers: Sequence[bytes]) -> Tuple[bytes, bytes]:

        while True:

            best_idx = None

            best_marker = None

            for m in markers:

                idx = self.buf.find(m)

                if idx != -1 and (best_idx is None or idx < best_idx):

                    best_idx = idx

                    best_marker = m

            if best_idx is not None and best_marker is not None:

                end = best_idx + len(best_marker)

                out = self.buf[:end]

                self.buf = self.buf[end:]

                return out, best_marker

            try:

                chunk = self.sock.recv(4096)

            except socket.timeout as e:

                preview = self.buf.decode(errors="replace")

                raise RuntimeError(

                    f"Socket timeout while waiting for one of {markers!r}. "

                    f"Buffered data so far:\n{preview}"

                ) from e

            if not chunk:

                out = self.buf

                self.buf = b""

                return out, b""

            self.buf += chunk

 

    def recv_until(self, marker: bytes) -> bytes:

        data, _ = self.recv_until_any([marker])

        return data

 

    def drain_until_close_or_timeout(self) -> bytes:

        chunks = [self.buf]

        self.buf = b""

        while True:

            try:

                chunk = self.sock.recv(4096)

            except socket.timeout:

                break

            if not chunk:

                break

            chunks.append(chunk)

        return b"".join(chunks)

 

 

def unshift_right(x: int, shift: int) -> int:

    res = x & 0xFFFFFFFF

    for _ in range(32):

        res = x ^ (res >> shift)

    return res & 0xFFFFFFFF

 

 

def unshift_left(x: int, shift: int, mask: int) -> int:

    res = x & 0xFFFFFFFF

    for _ in range(32):

        res = x ^ ((res << shift) & mask)

    return res & 0xFFFFFFFF

 

 

def untemper(v: int) -> int:

    v = unshift_right(v, 18)

    v = unshift_left(v, 15, 0xEFC60000)

    v = unshift_left(v, 7, 0x9D2C5680)

    v = unshift_right(v, 11)

    return v & 0xFFFFFFFF

 

 

def invert_step(si: int, si227: int) -> Tuple[int, int]:

    x = (si ^ si227) & 0xFFFFFFFF

    mti1 = (x & 0x80000000) >> 31

    if mti1:

        x ^= 0x9908B0DF

    x = (x << 1) & 0xFFFFFFFF

    mti = x & 0x80000000

    mti1 = (mti1 + (x & 0x7FFFFFFF)) & 0xFFFFFFFF

    return mti, mti1

 

 

def init_genrand(seed: int) -> List[int]:

    mt = [0] * 624

    mt[0] = seed & 0xFFFFFFFF

    for i in range(1, 624):

        mt[i] = (0x6C078965 * (mt[i - 1] ^ (mt[i - 1] >> 30)) + i) & 0xFFFFFFFF

    return mt

 

 

def recover_kj_from_ji(ji: int, ji1: int, i: int) -> int:

    const = init_genrand(19650218)

    key = ji - (const[i] ^ (((ji1 ^ (ji1 >> 30)) * 1664525) & 0xFFFFFFFF))

    return key & 0xFFFFFFFF

 

 

def recover_ji_from_ii(ii: int, ii1: int, i: int) -> int:

    ji = (ii + i) ^ (((ii1 ^ (ii1 >> 30)) * 1566083941) & 0xFFFFFFFF)

    return ji & 0xFFFFFFFF

 

 

def recover_kj_from_ii(ii: int, ii1: int, ii2: int, i: int) -> int:

    ji = recover_ji_from_ii(ii, ii1, i)

    ji1 = recover_ji_from_ii(ii1, ii2, i - 1)

    return recover_kj_from_ji(ji, ji1, i)

 

 

def recover_seed_candidates(obs: Dict[int, int]) -> Tuple[int, int]:

    s = {i: untemper(v) for i, v in obs.items()}

 

    i_229_msb, i_230 = invert_step(s[2], s[229])

    i_230_msb, i_231 = invert_step(s[3], s[230])

    i_231_msb, i_232 = invert_step(s[4], s[231])

    i_232_msb, i_233 = invert_step(s[5], s[232])

 

    i_230 = (i_230 + i_230_msb) & 0xFFFFFFFF

    i_231 = (i_231 + i_231_msb) & 0xFFFFFFFF

    i_232 = (i_232 + i_232_msb) & 0xFFFFFFFF

 

    seed_hi = (recover_kj_from_ii(i_232, i_231, i_230, 232) - 1) & 0xFFFFFFFF

    seed_lo_1 = recover_kj_from_ii(i_233, i_232, i_231, 233) & 0xFFFFFFFF

    seed_lo_2 = recover_kj_from_ii((i_233 + 0x80000000) & 0xFFFFFFFF, i_232, i_231, 233) & 0xFFFFFFFF

 

    cand1 = (seed_hi << 32) | seed_lo_1

    cand2 = (seed_hi << 32) | seed_lo_2

    return cand1, cand2

 

 

def output6_from_seed(seed: int) -> int:

    r = random.Random(seed)

    r.getrandbits(64)

    outs = [r.getrandbits(32) for _ in range(5)]

    return outs[4]

 

 

def uuid1_from_parts(timestamp_100ns: int, node: int, clock_seq: int) -> uuid.UUID:

    time_low = timestamp_100ns & 0xFFFFFFFF

    time_mid = (timestamp_100ns >> 32) & 0xFFFF

    time_hi_version = (timestamp_100ns >> 48) & 0x0FFF

    clock_seq_low = clock_seq & 0xFF

    clock_seq_hi_variant = (clock_seq >> 8) & 0x3F

    return uuid.UUID(

        fields=(time_low, time_mid, time_hi_version, clock_seq_hi_variant, clock_seq_low, node),

        version=1,

    )

 

 

def uuid6_from_parts(timestamp_100ns: int, node: int, clock_seq: int) -> uuid.UUID:

    time_hi_and_mid = (timestamp_100ns >> 12) & 0xFFFFFFFFFFFF

    time_lo = timestamp_100ns & 0x0FFF

    clock_s = clock_seq & 0x3FFF

    int_uuid = (time_hi_and_mid << 80) | (time_lo << 64) | (clock_s << 48) | (node & 0xFFFFFFFFFFFF)

    int_uuid |= FLAG_V6

    return uuid.UUID(int=int_uuid)

 

 

def uuid8_from_rng(rng: random.Random) -> uuid.UUID:

    a = rng.getrandbits(48)

    b = rng.getrandbits(12)

    c = rng.getrandbits(62)

    int_uuid = ((a & 0xFFFFFFFFFFFF) << 80) | ((b & 0xFFF) << 64) | (c & 0x3FFFFFFFFFFFFFFF)

    int_uuid |= FLAG_V8

    return uuid.UUID(int=int_uuid)

 

 

def hash_line_parts(block: str) -> Tuple[str, str]:

    m = re.search(r"hint: ([0-9a-f]{8})\.\.\.@sha256:([0-9a-f]{64})", block)

    if not m:

        raise RuntimeError(f"Could not parse hint/hash from:\n{block}")

    return m.group(1), m.group(2)

 

 

def failure_parts(block: str) -> Tuple[str, int]:

    m = re.search(r"Wrong\. It was: ([0-9a-f-]+) with salt ([0-9a-f]+)", block)

    if not m:

        raise RuntimeError(f"Could not parse failure line from:\n{block}")

    return m.group(1), int(m.group(2), 16)

 

 

def choose_seed(cand1: int, cand2: int, observed_output6: int) -> int:

    if output6_from_seed(cand1) == observed_output6:

        return cand1

    if output6_from_seed(cand2) == observed_output6:

        return cand2

    raise RuntimeError("Neither recovered seed candidate matches output #6")

 

 

def advance_rng_through_sacrifices(rng: random.Random) -> None:

    for _ in range(5):

        rng.getrandbits(32)

    for _ in range(7):

        rng.getrandbits(48)

        rng.getrandbits(14)

        rng.getrandbits(32)

    for _ in range(3):

        rng.getrandbits(2026)

        rng.getrandbits(32)

    for _ in range(3):

        rng.getrandbits(32)

 

 

def sha_matches(u: uuid.UUID, salt: bytes, pepper: bytes, digest_hex: str) -> bool:

    return hashlib.sha256(u.bytes + salt + pepper).hexdigest() == digest_hex

 

 

def recv_version_prompt(tube: Tube) -> str:

    if tube.at_version_prompt:

        tube.at_version_prompt = False

        return ""

    data, marker = tube.recv_until_any([

        b"Version (1-8): ",

        b"Congratulations!",

        b"Out of guesses!",

    ])

    text = data.decode(errors="replace")

    if marker == b"Version (1-8): ":

        return text

    raise RuntimeError(f"Session ended before next prompt:\n{text}")

 

 

def do_failed_attempt(tube: Tube, version: int, count: int) -> Tuple[str, str, int, int]:

    recv_version_prompt(tube)

    tube.sendline(str(version))

    tube.recv_until(b"How many UUIDs to generate before guessing?: ")

    tube.sendline(str(count))

    hint_block = tube.recv_until(b"Your guess: ").decode(errors="replace")

    t_hint_ns = time.time_ns()

    tube.sendline(WRONG_GUESS)

    result_block, marker = tube.recv_until_any([

        b"Version (1-8): ",

        b"Congratulations!",

        b"Out of guesses!",

    ])

    result_text = result_block.decode(errors="replace")

    target_str, salt_int = failure_parts(result_text)

    if marker == b"Version (1-8): ":

        tube.at_version_prompt = True

    else:

        raise RuntimeError(f"Unexpected end of session during sacrifice:\n{result_text}")

    return hint_block, target_str, salt_int, t_hint_ns

 

 

def do_count1_and_capture_hint(tube: Tube, version: int) -> Tuple[str, str, int]:

    recv_version_prompt(tube)

    tube.sendline(str(version))

    tube.recv_until(b"How many UUIDs to generate before guessing?: ")

    tube.sendline("1")

    hint_block = tube.recv_until(b"Your guess: ").decode(errors="replace")

    t_hint_ns = time.time_ns()

    hint_hex, digest_hex = hash_line_parts(hint_block)

    return hint_hex, digest_hex, t_hint_ns

 

 

def send_guess_and_check(tube: Tube, guess: str) -> str:

    tube.sendline(guess)

    post, marker = tube.recv_until_any([

        b"Version (1-8): ",

        b"Congratulations!",

        b"Out of guesses!",

    ])

    if marker == b"Version (1-8): ":

        tube.at_version_prompt = True

        return post.decode(errors="replace")

 

    if marker in (b"Congratulations!", b"Out of guesses!"):

        tail = tube.drain_until_close_or_timeout()

        return (post + tail).decode(errors="replace")

 

    return post.decode(errors="replace")

 

 

def predict_v3(rng: random.Random, digest_hex: str, pepper: bytes) -> uuid.UUID:

    u = uuid.uuid3(uuid.NAMESPACE_DNS, str(rng.getrandbits(2026)))

    salt = rng.getrandbits(32).to_bytes(4, "big")

    if not sha_matches(u, salt, pepper, digest_hex):

        raise RuntimeError("v3 prediction mismatch")

    return u

 

 

def predict_v5(rng: random.Random, digest_hex: str, pepper: bytes) -> uuid.UUID:

    u = uuid.uuid5(uuid.NAMESPACE_DNS, str(rng.getrandbits(2026)))

    salt = rng.getrandbits(32).to_bytes(4, "big")

    if not sha_matches(u, salt, pepper, digest_hex):

        raise RuntimeError("v5 prediction mismatch")

    return u

 

 

def predict_v8(rng: random.Random, digest_hex: str, pepper: bytes) -> uuid.UUID:

    u = uuid8_from_rng(rng)

    salt = rng.getrandbits(32).to_bytes(4, "big")

    if not sha_matches(u, salt, pepper, digest_hex):

        raise RuntimeError("v8 prediction mismatch")

    return u

 

 

def predict_v1(

    rng: random.Random,

    hint_hex: str,

    digest_hex: str,

    pepper: bytes,

    t_hint_ns: int,

    remote_offset_100ns: int,

) -> Tuple[uuid.UUID, int, int, int]:

    node = rng.getrandbits(48)

    clock_seq = rng.getrandbits(14)

    salt = rng.getrandbits(32).to_bytes(4, "big")

 

    approx = (t_hint_ns // 100) + UUID_EPOCH_100NS + remote_offset_100ns

    hint_low32 = int(hint_hex, 16)

    base = (approx & ~0xFFFFFFFF) | hint_low32

 

    candidates = [base + wrap * (1 << 32) for wrap in range(-2, 3)]

    candidates.sort(key=lambda x: abs(x - approx))

 

    for ts in candidates:

        u = uuid1_from_parts(ts, node, clock_seq)

        if sha_matches(u, salt, pepper, digest_hex):

            return u, ts, node, clock_seq

 

    raise RuntimeError("Could not match v1 timestamp")

 

 

def predict_v6(

    rng: random.Random,

    hint_hex: str,

    digest_hex: str,

    pepper: bytes,

    t_hint_ns: int,

    remote_offset_100ns: int,

) -> Tuple[uuid.UUID, int, int, int]:

    node = rng.getrandbits(48)

    clock_seq = rng.getrandbits(14)

    salt = rng.getrandbits(32).to_bytes(4, "big")

 

    approx = (t_hint_ns // 100) + UUID_EPOCH_100NS + remote_offset_100ns

    hint_hi32 = int(hint_hex, 16)

    base = (hint_hi32 << 28) | (approx & ((1 << 28) - 1))

 

    for window_ms in (1, 2, 5, 10, 20, 50, 100, 250, 500):

        span = window_ms * 10_000

        for delta in range(span + 1):

            if delta == 0:

                ts = base

                u = uuid6_from_parts(ts, node, clock_seq)

                if sha_matches(u, salt, pepper, digest_hex):

                    return u, ts, node, clock_seq

                continue

            for ts in (base + delta, base - delta):

                u = uuid6_from_parts(ts, node, clock_seq)

                if sha_matches(u, salt, pepper, digest_hex):

                    return u, ts, node, clock_seq

 

    raise RuntimeError("Could not match v6 timestamp within 500 ms window")

 

 

def exploit(host: str, port: int) -> None:

    tube = Tube(host, port)

    try:

        observed: Dict[int, int] = {}

 

        # 1-5: leak outputs 2..6 via v4 count=1 failures.

        for pos in range(2, 7):

            _, _, salt_int, _ = do_failed_attempt(tube, 4, 1)

            observed[pos] = salt_int

            print(f"[+] Leaked output {pos}: {salt_int:08x}")

 

        # 6: burn 28 outputs with v1 count=7. This also gives us one real remote v1 timestamp.

        _, v1_last_target, _, t_v1_hint_ns = do_failed_attempt(tube, 1, 7)

        remote_v1 = uuid.UUID(v1_last_target)

        remote_offset_100ns = remote_v1.time - ((t_v1_hint_ns // 100) + UUID_EPOCH_100NS)

        print(f"[+] Estimated remote clock offset (100ns units): {remote_offset_100ns}")

 

        # 7: burn 195 outputs with v3 count=3; leak output 229 as its final salt.

        _, _, salt_229, _ = do_failed_attempt(tube, 3, 3)

        observed[229] = salt_229

        print(f"[+] Leaked output 229: {salt_229:08x}")

 

        # 8-10: leak outputs 230..232.

        for pos in (230, 231, 232):

            _, _, salt_int, _ = do_failed_attempt(tube, 4, 1)

            observed[pos] = salt_int

            print(f"[+] Leaked output {pos}: {salt_int:08x}")

 

        needed = {2, 3, 4, 5, 229, 230, 231, 232}

        c1, c2 = recover_seed_candidates({k: observed[k] for k in needed})

        seed = choose_seed(c1, c2, observed[6])

        print(f"[+] Recovered seed: 0x{seed:016x}")

 

        rng = random.Random(seed)

        pepper = rng.getrandbits(64).to_bytes(8, "big")

        advance_rng_through_sacrifices(rng)

 

        # Solve v1 first so we can refresh the remote clock offset with an exact new timestamp.

        for version in (1, 6, 8, 3, 5):

            hint_hex, digest_hex, t_hint_ns = do_count1_and_capture_hint(tube, version)

 

            if version == 1:

                guess_uuid, ts, _, _ = predict_v1(rng, hint_hex, digest_hex, pepper, t_hint_ns, remote_offset_100ns)

                remote_offset_100ns = ts - ((t_hint_ns // 100) + UUID_EPOCH_100NS)

                print(f"[+] v1 = {guess_uuid}")

            elif version == 6:

                guess_uuid, _, _, _ = predict_v6(rng, hint_hex, digest_hex, pepper, t_hint_ns, remote_offset_100ns)

                print(f"[+] v6 = {guess_uuid}")

            elif version == 8:

                guess_uuid = predict_v8(rng, digest_hex, pepper)

                print(f"[+] v8 = {guess_uuid}")

            elif version == 3:

                guess_uuid = predict_v3(rng, digest_hex, pepper)

                print(f"[+] v3 = {guess_uuid}")

            elif version == 5:

                guess_uuid = predict_v5(rng, digest_hex, pepper)

                print(f"[+] v5 = {guess_uuid}")

            else:

                raise AssertionError("unreachable")

 

            result = send_guess_and_check(tube, str(guess_uuid))

            if "Correct!" not in result and "Congratulations!" not in result:

                raise RuntimeError(f"Prediction for version {version} failed:\n{result}")

            print(result.strip())

 

            flag_match = re.search(r"Here is your flag: (.+)", result)

            if flag_match:

                print(flag_match.group(1))

                return

 

        raise RuntimeError("Solved 5 versions but flag was not found in output")

    finally:

        tube.close()

 

 

def main() -> None:

    parser = argparse.ArgumentParser(description="Exploit the uuid-guesser challenge")

    parser.add_argument("host", nargs="?", default="uuid-guesser.cfire")

    parser.add_argument("port", nargs="?", type=int, default=1337)

    args = parser.parse_args()

    exploit(args.host, args.port)

 

 

if __name__ == "__main__":

    main()