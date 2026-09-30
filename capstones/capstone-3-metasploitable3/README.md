# Capstone Project 3 — Penetration Testing (Metasploitable 3)

## Overview
Internal security assessment of a simulated legacy development environment
(Metasploitable 3) conducted as part of the Moringa School cybersecurity
capstone. The assessment covered reconnaissance, enumeration, exploitation,
post-exploitation, and risk reporting against a deliberately vulnerable
Ubuntu 14.04 target.

**Target:** Metasploitable 3 | IP: 10.0.2.3  
**OS:** Ubuntu 14.04.6 LTS (EOL)  
**Assessment Date:** September 2026  
**Course:** Moringa School — CSFB-FT09M6  

---

## Group Project
This was a group capstone. Each group member conducted independent
penetration testing against their own Metasploitable 3 instance and
contributed findings to the shared deliverables.

**My contributions:**
- Independent penetration test (reconnaissance through root compromise)
- Showcase slide deck (20-slide presentation built on the course template)
- port_scanner.py and web_scanner.py (independently written and tested)
- Penetration test report sections covering my own test findings

---

## Key Findings
| Severity | Count | Examples |
|----------|-------|---------|
| Critical | 3 | ProFTPD RCE, UnrealIRCd Backdoor, Default SSH Credentials |
| High | 3 | Drupal 7.5, SMB guest access, EOL OS |
| Medium | 3 | Reflected XSS, MySQL exposed, Outdated services |

**Attack chain:**  
ProFTPD mod_copy (CVE-2015-3306) → www-data shell → Meterpreter →  
UnrealIRCd backdoor (CVE-2010-2075) → boba_fett → su vagrant → sudo → root

---

## Custom Scripts

### port_scanner.py
TCP port scanner using Python `socket` module only (no external libraries).
- Concurrent scanning via `concurrent.futures.ThreadPoolExecutor`
- Banner grabbing on open ports (passive + HTTP HEAD fallback)
- Accepts target via CLI argument or interactive prompt
- PEP8 compliant

```bash
python3 port_scanner.py 10.0.2.3 -p 1-65535 -w 50
```

### web_scanner.py
Reflected XSS scanner using Python `requests` module.
- Tests multiple payload variants including URL-encoded/obfuscated forms
- Aligned with OWASP Top 10 A03:2021 (Injection / XSS)
- Per-payload result output + summary count

```bash
# Start the vulnerable test app first
python3 app.py

# Run the scanner
python3 web_scanner.py
```

---

## Deliverables
- `pitch/` — Project pitch (scope, methodology, timeline, success metrics)
- `report/` — Full penetration test report
- `scripts/` — port_scanner.py and web_scanner.py
- `slides/` — Showcase presentation deck

---

## Tools Used
- Nmap 7.98
- Metasploit Framework
- Kali Linux
- Python 3 (socket, requests, concurrent.futures, argparse)
- smbclient, curl, searchsploit

---

## Disclaimer
All testing was conducted against an isolated, authorized lab environment
(VirtualBox NAT Network). No live or unauthorized systems were accessed.
