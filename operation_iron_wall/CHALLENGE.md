# Operation Iron Wall — CTF Challenge

**Scenario:** Your organization has been hit by a sophisticated attacker. 
You are the Blue Team analyst tasked with investigating the breach. 
Analyze the evidence, contain the threat, and extract the flags.

**Flag Format:** `0xmr{...}`

**Difficulty:** Medium-Hard  
**Category:** DFIR (Digital Forensics & Incident Response)  
**Total Points:** 1000 (4 tasks × 250 pts)

---

## Task 1: Log Analysis (250 pts)

**Files:** `task1/access.log`

Analyze the Apache access log. The attacker brute-forced the login then 
performed SQL injection. Find the exact UTC timestamp (HHMMSS) of the 
first successful SQLi request (200 status after repeated 401/403).

**Flag format:** `0xmr{HHMMSS}`

**Hints:**
- Look for POST /api/auth/login requests
- The attacker IP is 198.51.100.77
- The first successful SQLi will have HTTP 200 after many 401/403 responses
- The timestamp is in UTC, extract just HHMMSS

---

## Task 2: Network Analysis (250 pts)

**Files:** `task2/dns_capture.txt`, `task2/dns_queries_raw.txt`

Examine the network capture. Data was exfiltrated via DNS tunneling. 
Decode the base64 payload from the DNS queries and extract the hidden flag string.

**Hints:**
- Look for DNS queries to `update-cdn-service.com`
- The subdomains contain base64-encoded data
- Concatenate all base64 chunks and decode
- The raw hex dump file contains the same data in hex format

---

## Task 3: Binary Analysis (250 pts)

**Files:** `task3/svc_monitor`, `task3/strings_output.txt`, `task3/analysis_notes.txt`

A suspicious binary was found on the compromised server. Statically analyze it — 
find the hardcoded C2 URL, decode the XOR-encoded string (key: 0x42), and 
extract the flag from the config payload.

**Hints:**
- Use `strings` or the provided strings output
- Look for the XOR-encoded hex dumps
- XOR key is 0x42 (decimal 66, ASCII 'B')
- The flag is in the second encrypted string
- Decrypt: XOR each byte with 0x42

---

## Task 4: Timeline Analysis (250 pts)

**Files:** `task4/incident_timeline.txt`

Review the incident timeline: the attacker exploited a vulnerable service, 
established persistence via cron, and lateral-moved to 3 hosts. 
Calculate total compromised unique IPs and identify the exploited service.

**Flag format:** `0xmr{service_total_ips}`

**Hints:**
- Count ALL unique IPs in the compromise (including attacker infrastructure)
- The exploited service is mentioned multiple times in the timeline
- The format is: service name (lowercase) + underscore + total count
- Total IPs = initial host + 3 lateral moved hosts + attacker C2 = 5

---

## Solutions

<details>
<summary>Click to reveal solutions (spoiler warning!)</summary>

### Task 1
**Flag:** `0xmr{143822}`

The first successful SQLi request occurs at 15/Jul/2026:14:38:22 UTC.
Look for POST /api/auth/login returning HTTP 200 after the long sequence
of 401 and 403 responses.

### Task 2
**Flag:** `0xmr{dn5_tun3l_m4lw4r3_15_r34l}`

The DNS queries to update-cdn-service.com contain base64-encoded subdomains.
Concatenate all subdomain labels and base64-decode the result.

### Task 3
**Flag:** `0xmr{c0ld_pr0be_1nj3ct10n_m4lw4r3}`

XOR the second encrypted hex string with key 0x42 to decode.
The C2 URL is: https://dark-relay.c2-server.xyz/beacon

### Task 4
**Flag:** `0xmr{openssh_5}`

Total compromised unique IPs: 5
- 10.0.1.13 (prod-web-03)
- 10.0.1.15 (db-primary-01)
- 10.0.1.22 (app-worker-01)
- 10.0.1.8 (monitoring-01)
- 198.51.100.77 (attacker C2)

Exploited service: openssh

</details>
