heard that UUID is pretty random, but is it really? Can you still somehow guess the various UUID versions correctly?
uuid-guesser.cfire:1337

Handout
sha256: 66a2ac950e006b9e72f7cb234b5c033c267416416ef192d79118e2ce914d0407

NOTE: Create a user and find the VPN and Browser LABs on Campfire Labs:



nc uuid-guesser.cfire 1337
---------------------------------------------------
 Welcome to the UUID Guesser!
 - Choose a UUID version (1-8)
 - You have 15 total attempts
 - Solve 5 different UUIDs to get the flag
---------------------------------------------------

Solved: 0/5 | Remaining attempts: 15
Version (1-8):




jma@jens-pc:/mnt/c/workspace/ddc/2026/CALL_ME_MAYBE/call_me_maybe$ nc uuid-guesser.cfire 1337
---------------------------------------------------
 Welcome to the UUID Guesser!
 - Choose a UUID version (1-8)
 - You have 15 total attempts
 - Solve 5 different UUIDs to get the flag
---------------------------------------------------

Solved: 0/5 | Remaining attempts: 15
Version (1-8): 1
How many UUIDs to generate before guessing?: 10
[1] UUIDv1 hint: 07cdac21...@sha256:442a4fd32d7437a2464b0c7e55b7b7857a6f55655123fff818fdb9c4decc78f4
[2] UUIDv1 hint: 07cdafd4...@sha256:b993c66829bba4437a3ee90bbbc6bc61907d588b4bbc10950f5b5c676da755aa
[3] UUIDv1 hint: 07cdb3d7...@sha256:8607176bd8611688ff60f8fe3176e4bbb99762d0da3db16eee651933e93b9ab1
[4] UUIDv1 hint: 07cdb434...@sha256:fda1e828410548ea19684e53007d243c73bd6c760e824bae9482f455abaf8632
[5] UUIDv1 hint: 07cdb47a...@sha256:8342a2f8bda6b33afd25b8c3a7c7798fdd78a7896fcf878256a9f5ab9278f77d
[6] UUIDv1 hint: 07cdb4c4...@sha256:291683c4ce5e68ddf2c04a9bedcf7d18ae1ecd880dc3bede6538c95a5a91dd39
[7] UUIDv1 hint: 07cdb501...@sha256:19ae59a522ce14c218ac243721843bc4a307a03e3793f6650940a73a62964292
[8] UUIDv1 hint: 07cdb53b...@sha256:a74c9e748ea8e2c437dc1aefa8e28c99121803abd3fe7f583519f5385ebb4294
[9] UUIDv1 hint: 07cdb573...@sha256:0d38a5a8d17c7f601d18ed76ce8a38a76b64357d4a69a23ba9ef040994cf90f1
[10] UUIDv1 hint: 07cdb5a9...@sha256:82d6eed5a0fa1a16aa750f708ad06267e4e721fe790abbb3d3073cc69b47232d




            target = generate_uuid(version)
            SALT = random.getrandbits(32).to_bytes(4)
            hint = target.bytes[:4].hex() 
            print(f"[{i+1}] UUIDv{version} hint: {hint}...@sha256:{hashlib.sha256(target.bytes + SALT + PEPPER).hexdigest()}")

            getrandbits(32) er MT... PEPPER er fast.  sha256 laves for hele værdier... 

            HVIS man kunne finde 

            PEPPER = random.getrandbits(64).to_bytes(8)

            Vi har uuid 16 bytes
            Pebber  8 bytes
            salt 4 byte

            