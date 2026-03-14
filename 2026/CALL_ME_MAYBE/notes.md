Du er lige startet i praktik hos NoTech, en banebrydende startup inden for cybersikkerhed.
Allerede på din allerførste dag kommer din manager forbi dit skrivebord og skubber et USB-drev hen over bordet.

"Analytikeren før dig efterlod den her.
Det er en form for låst terminal; ingen her kender adgangskoden.
Vi har prøvet alt. Tror du, du kan knække den, rookie?"*

Hun blinker og går videre. Du sætter USB’en i og finder én enkelt fil: call_me_maybe.
Du kører den. Den beder om en adgangskoden. Du har den ikke.
Men der er noget ved navnet, der nager dig… Call Me Maybe… calls… maybe?

Hvad hvis hemmeligheden ikke ligger inde i programmet, men i det, programmet kalder?




elf file unpacked has DDC text, but not complete

https://www.sunshine2k.de/coding/javascript/onlineelfviewer/onlineelfviewer.html


jma@jens-pc:/mnt/c/workspace/ddc/2026/CALL_ME_MAYBE/call_me_maybe$ ltrace  ./call_me_maybe
setvbuf(0x73b8ac61b780, 0, 2, 0)                                          = 0
putchar(10, 0, 125, 3072
)                                                 = 10
puts("  \342\225\224\342\225\220\342\225\220\342\225\220\342\225\220\342\225\220\342\225\220\342\225\220\342\225\220\342\225\220"...  ╔══════════════════════════════════════════╗
) = 135
puts("  \342\225\221      NoTech Security Termi"...  ║      NoTech Security Terminal v2.4       ║
)                      = 51
puts("  \342\225\221        Authentication Requ"...  ║        Authentication Required           ║
)                      = 51
puts("  \342\225\232\342\225\220\342\225\220\342\225\220\342\225\220\342\225\220\342\225\220\342\225\220\342\225\220\342\225\220"...  ╚══════════════════════════════════════════╝
) = 135
putchar(10, 1, 1, 0x73b8ac514907
)                                         = 10
puts("  STATUS: 1 classified message w"...  STATUS: 1 classified message waiting
)                               = 39
puts("  CLEARANCE: Agent-level passphr"...  CLEARANCE: Agent-level passphrase required

)                               = 46
printf("  Enter passphrase: "  Enter passphrase: )                                            = 20
fgets(test
"test\n", 256, 0x73b8ac61aaa0)                                      = 0x7fff96a3b1a0
strcspn("test\n", "\n")                                                   = 4
strcmp("test", "DDC{ltr4c3_my_l1br4ry_c4lls}")                            = 48
puts("\n  [ACCESS DENIED]"
  [ACCESS DENIED]
)                                               = 19
puts("  Invalid passphrase. Terminal l"...  Invalid passphrase. Terminal locked.

)                               = 40
puts("  Hint: Maybe you should trace t"...  Hint: Maybe you should trace the calls...

)                               = 45
+++ exited (status 0) +++
jma@jens-pc:/mnt/c/workspace/ddc/2026/CALL_ME_MAYBE/call_me_maybe$