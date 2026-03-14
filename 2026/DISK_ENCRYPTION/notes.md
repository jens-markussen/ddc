Jeg implementerede min egen diskkrypteringstjeneste ved hjælp af standard AES-XTS-tilstanden.

Den er stadig i beta, så jeg har inkluderet en fejlfindingstilstand, som brugerne kan prøve.
Det er ikke et sikkerhedsproblem, fordi den kun krypterer ved hjælp af ECB, og ingen andre kender nøglen. Kun administratorbrugere kan læse nøglen alligevel.

Kan man hacke den?

nc diskenc.cfire 1337

Download
sha256: 56202e94379438fa982c71239e5f0e56bc60c8ed6cbb972e76a7cb534023c128

NOTE: Create a user and find the VPN and Browser LABs on Campfire Labs:

https://kvalifikation.campfiresecurity.dk/challenges?challenge=disk-encryption



Creating account there. After that this links gives:

Disk Encryption
1000
Jeg implementerede min egen diskkrypteringstjeneste ved hjælp af standard AES-XTS-tilstanden.

Den er stadig i beta, så jeg har inkluderet en fejlfindingstilstand, som brugerne kan prøve. Det er ikke et sikkerhedsproblem, fordi den kun krypterer ved hjælp af ECB, og ingen andre kender nøglen. Kun administratorbrugere kan læse nøglen alligevel.

Kan man hacke den?

Handout SHA256: 56202e94379438fa982c71239e5f0e56bc60c8ed6cbb972e76a7cb534023c128

nc diskenc.cfire 1337



nc er netcat kommando. Skal jeg VPN'e ind først?

Laver et "VPN laboratorium", som man kan forbinde til via wireguard

Tilføjet til Wireguard og forbundet med success!


jma@jens-pc:~$ nc diskenc.cfire 1337
nc: getaddrinfo for host "diskenc.cfire" port 1337: Name or service not known

Hvis man så starter servicen, så er der faktisk noget i den anden ende.

jma@jens-pc:~$ nc diskenc.cfire 1337
File 'passwd' encrypted in memory.

For debugging purposes, I can encrypt two blocks under ECB.



Hvis man skriver noget, så går python serveren ned:

jma@jens-pc:~$ nc diskenc.cfire 1337
File 'passwd' encrypted in memory.

For debugging purposes, I can encrypt two blocks under ECB.

Traceback (most recent call last):
  File "server.py", line 62, in <module>
    assert(len(debug) == 2)
AssertionError
passwd
jma@jens-pc:~$ nc diskenc.cfire 1337
File 'passwd' encrypted in memory.

For debugging purposes, I can encrypt two blocks under ECB.




jma@jens-pc:~$ nc diskenc.cfire 1337
File 'passwd' encrypted in memory.

For debugging purposes, I can encrypt two blocks under ECB.
FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
9bcc91bc4a91481b8066a9be2f3933eb 2fedeb3badd5bc7a89f8b2300469b702

For debugging purposes, I can also restore an encrypted block in memory, just give me number and contents (but do not change usernames).


00000000000000000000000000000000 00000000000000000000000000000000

File 'passwd' encrypted in memory.

For debugging purposes, I can encrypt two blocks under ECB.
00000000000000000000000000000000 00000000000000000000000000000000
59ef1f82d2959c119b42db7701b36052 f9dc2f0101f96f531ba373216e31b9a5

For debugging purposes, I can also restore an encrypted block in memory, just give me number and contents (but do not change usernames)



Claude siger

Interesting! Two identical plaintext blocks produced different ciphertexts:

Block 0: 59ef1f82d2959c119b42db7701b36052
Block 1: f9dc2f0101f96f531ba373216e31b9a5

This confirms XTS mode — the block index is used as a tweak, so even identical plaintexts encrypt differently depending on their position.
The attack plan:
The "restore" feature lets you overwrite encrypted blocks in the passwd file. Since the debug oracle encrypts with position 0 or 1 as tweak, you can forge a valid ciphertext for block 0 or 1 of the passwd file.
Next step — encrypt a crafted passwd entry. A typical /etc/passwd root line is 32 bytes (2 blocks). Try encrypting something like:
['726f6f743a783a303a303a726f6f743a', '2f726f6f743a2f62696e2f6261736800']
That's root:x:0:0:root: and /root:/bin/bash\0 in hex.
Then use the restore feature to write those blocks back. What does the encrypted passwd currently look like — can you dump the block numbers and contents from the server?


----


00000000000000000000000000000000 00000000000000000000000000000000
59ef1f82d2959c119b42db7701b36052 f9dc2f0101f96f531ba373216e31b9a5



>>> hex(0x59ef1f82d2959c119b42db7701b36052 ^ 0xf9dc2f0101f96f531ba373216e31b9a5)
'0xa0333083d36cf34280e1a8566f82d9f7'


11111111111111111111111111111111 11111111111111111111111111111111

For debugging purposes, I can encrypt two blocks under ECB.
11111111111111111111111111111111 11111111111111111111111111111111
df35789f2b348bf3959a90f467c0ec99 b6ca6483302d55a565cde926651ddf7f


hex(0xdf35789f2b348bf3959a90f467c0ec99 ^0xb6ca6483302d55a565cde926651ddf7f)

>>> hex(0xdf35789f2b348bf3959a90f467c0ec99 ^0xb6ca6483302d55a565cde926651ddf7f)
'0x69ff1c1c1b19de56f05779d202dd33e6'

0 block
hex(0x59ef1f82d2959c119b42db7701b36052 ^0xdf35789f2b348bf3959a90f467c0ec99)
'0x86da671df9a117e20ed84b8366738ccb'

1 blcok
>>> hex(0xf9dc2f0101f96f531ba373216e31b9a5 ^ 0xb6ca6483302d55a565cde926651ddf7f)
'0x4f164b8231d43af67e6e9a070b2c66da'




726f6f743a3a303a303a3a2f3a0a0000
Which is root::0:0::/:\n\x00\x00 — send this as block 0 to the oracle, then restore with 0 <CT[0]>.


block 0 XOR

00000000000000000000000000000000 00000000000000000000000000000000
59ef1f82d2959c119b42db7701b36052 f9dc2f0101f96f531ba373216e31b9a5

11111111111111111111111111111111 11111111111111111111111111111111
df35789f2b348bf3959a90f467c0ec99 b6ca6483302d55a565cde926651ddf7f

22222222222222222222222222222222 22222222222222222222222222222222
6f6e6041fee5dd6d0b863115a72a561f 97b79f56772001d5ae0e2e2fbf47f340

hex(0x59ef1f82d2959c119b42db7701b36052 ^ 0x11111111111111111111111111111111)
'0x48fe0e93c3848d008a53ca6610a27143'

hex(0x59ef1f82d2959c119b42db7701b36052 ^ 0x11111111111111111111111111111111)


trying to update blocks gives user warnings up to e.g. 180.

200 is out of range, but e.g. 190 just accepts it.


Escape character is '^]'.
File 'passwd' encrypted in memory.

For debugging purposes, I can encrypt two blocks under ECB.
726f6f743a3a303a303a3a2f3a0a0000 726f6f743a3a303a303a3a2f3a0a0000
44d37ca1c187f716316a19fd09c42d0f 1e6bd0e0e8cc36a66ef37943acd50b17

For debugging purposes, I can also restore an encrypted block in memory, just give me number and contents (but do not change usernames).
190 726f6f743a3a303a303a3a2f3a0a0000

let's find limit

185 user error

188 user error

189 user error   This one is still part of the pw file, so 190 * 16 bytes = 3040 bytes in passwd file.

190 closes

191 closes

193 closes.   193 is the last block. So, there are 194 blocks * 16 bytes = 3104 bytes

194 too much

195 too much
