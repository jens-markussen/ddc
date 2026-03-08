 33 (97% liked)  1
Vi har en mistanke om, at nogen har lavet nogle mærkelige forespørgsler til vores server.
Kan du finde flaget?

Husk, at flagformatet er DDC{}

Download

sha256: afa319b9b44775af9065337067db74081965ea5d07d9689742b4246becd8e5d3


In log file searching

192.168.1.99 - - [28/Nov/2025:14:33:45 +0100] "GET /search.php?user_cookie=s0me_base64_c0de_DDC{Tim3_Tr4v3l HTTP/1.1" 200 1405 "-" "Mozilla/5.0 (Custom-Scanner; Log-Digger; PID:12345)"
10.0.0.8 - - [28/Nov/2025:14:33:46 +0100] "GET /about HTTP/1.1" 200 4810 "http://google.com/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
172.16.0.5 - - [28/Nov/2025:14:33:47 +0100] "GET /docs HTTP/1.1" 200 4538 "-" "Mozilla/5.0 (compatible; Googlebot/2.1)"
172.16.0.7 - - [28/Nov/2025:14:33:48 +0100] "GET /products HTTP/1.1" 200 516 "-" "Mozilla/5.0 (Linux; Android 10; SM-G973F)"
10.0.0.4 - - [28/Nov/2025:14:33:49 +0100] "GET /images/logo.png HTTP/1.1" 200 2355 "http://google.com/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
172.16.0.4 - - [28/Nov/2025:14:33:50 +0100] "GET /css/styles.css HTTP/1.1" 200 2318 "http://internal-wiki.com/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
172.16.0.3 - - [28/Nov/2025:14:33:51 +0100] "GET /about HTTP/1.1" 200 4296 "http://another-web-server.com/" "Mozilla/5.0 (compatible; Googlebot/2.1)"
10.0.0.9 - - [28/Nov/2025:14:33:52 +0100] "GET /css/styles.css HTTP/1.1" 200 2544 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
172.16.0.4 - - [28/Nov/2025:14:33:53 +0100] "GET /css/styles.css HTTP/1.1" 200 3784 "http://google.com/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
10.0.0.5 - - [28/Nov/2025:14:33:54 +0100] "GET / HTTP/1.1" 404 4747 "http://google.com/" "Mozilla/5.0 (Linux; Android 10; SM-G973F)"
172.16.0.8 - - [28/Nov/2025:14:33:55 +0100] "GET / HTTP/1.1" 200 2975 "-" "Mozilla/5.0 (Linux; Android 10; SM-G973F)"
172.16.0.3 - - [28/Nov/2025:14:33:56 +0100] "GET /docs HTTP/1.1" 404 2539 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
172.16.0.1 - - [28/Nov/2025:14:33:57 +0100] "GET /about HTTP/1.1" 404 923 "http://internal-wiki.com/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
172.16.0.5 - - [28/Nov/2025:14:33:58 +0100] "GET /about HTTP/1.1" 200 1089 "http://google.com/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
10.0.0.3 - - [28/Nov/2025:14:34:00 +0100] "GET /docs HTTP/1.1" 200 527 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
192.168.1.99 - - [28/Nov/2025:14:34:00 +0100] "GET /report.html HTTP/1.1" 200 1002 "http://internal.legacy-server.local/files/temp/_L0g_An4lys1s}/page.php" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"


Combining the two parts of the flag gives the correct answer: DDC{Tim3_Tr4v3l_L0g_An4lys1s}



