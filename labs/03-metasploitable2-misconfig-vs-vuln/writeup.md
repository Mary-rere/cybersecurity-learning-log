# Lab 03: Metasploitable2 — Misconfiguration vs. Vulnerability

**Date completed:** 2026-07-14
**Category:** Exploitation
**Tools used:** Netcat, Nmap, searchsploit, Metasploit Framework

## Objective
Compare two different root-compromise paths on the same target to understand the practical difference between a **misconfiguration** (an open door left by mistake) and a **vulnerability** (a flaw in the software itself that must be discovered and triggered).

## Environment
- Attacker machine: Kali Linux VM (192.168.56.102)
- Target: Metasploitable2 (192.168.56.101)
- Network setup: Isolated VirtualBox Host-only network

## Part A: Misconfiguration — Port 1524 Bindshell

### Steps Taken
Nmap recon had already flagged this port during earlier scanning:
<img width="1123" height="839" alt="Screenshot 2026-07-14 202456" src="https://github.com/user-attachments/assets/ec8d9f80-8fee-466a-81b1-11de32b68d29" />

No exploit or vulnerability research was needed — this port was already described as an open root shell. Connected directly:
<img width="627" height="384" alt="Screenshot 2026-07-14 210735" src="https://github.com/user-attachments/assets/656778be-2585-4c80-9c8d-7a7f4ad67b10" />

Verified access immediately:

<img width="664" height="383" alt="Screenshot 2026-07-14 210822" src="https://github.com/user-attachments/assets/3cddb5d5-3a31-4d58-bee9-61ba8e00e1c0" />

### Result
Instant root access — `uid=0(root) gid=0(root) groups=0(root)` — with no authentication, no exploit code, and no vulnerability research required. The service itself was deployed insecurely; there was nothing to "hack," only an open door to walk through.

## Part B: Vulnerability — UnrealIRCd 3.2.8.1 Backdoor

### Steps Taken
1. Confirmed the IRC service on port 6667 via Nmap
2. Searched for known exploits: `searchsploit unrealircd`
3. Identified a matching Metasploit module and reviewed its source, confirming the vulnerability as **CVE-2010-2075** — a malicious backdoor inserted into the official Unreal IRCD 3.2.8.1 download archive between November 2009 and June 2010
4. Ran the exploit:

<img width="1059" height="286" alt="Screenshot 2026-07-14 211754" src="https://github.com/user-attachments/assets/efa33c7a-7911-4f34-a628-34691e2a63bd" />
<img width="1049" height="128" alt="Screenshot 2026-07-14 212006" src="https://github.com/user-attachments/assets/4fe62600-66b4-4077-9d4e-073cafa70250" />
<img width="1041" height="117" alt="Screenshot 2026-07-14 212354" src="https://github.com/user-attachments/assets/65acb2c1-25c0-45ca-8796-cbe69462d84a" />
<img width="569" height="163" alt="Screenshot 2026-07-14 212434" src="https://github.com/user-attachments/assets/a4288949-11fd-4eaa-856c-0641e6237970" />

### Result
Achieved a root Meterpreter session by triggering a specific backdoor command over the IRC protocol — this required identifying the exact vulnerable version, researching the known CVE, and using a purpose-built exploit to activate malicious code hidden inside the software itself.

## Vulnerability vs. Misconfiguration

| | Misconfiguration (Port 1524) | Vulnerability (UnrealIRCd) |
|---|---|---|
| **Root cause** | Service deployed with no authentication | Malicious code planted in the software archive |
| **Discovery required?** | No — recon alone revealed it | Yes — required searchsploit, CVE research |
| **Trigger required?** | No — just connect | Yes — specific backdoor command via Metasploit |
| **Real-world fix** | Reconfigure/remove the exposed service | Patch/update the software |
| **CVE assigned?** | No | Yes (CVE-2010-2075) |

## What I Learned
- Not every compromise requires an exploit — misconfigurations can be just as damaging and are often easier to find and fix
- The practical difference in remediation: patching vs. reconfiguration
- Reinforced the full recon → research → exploit → verify methodology on a second, independent service

## What I'd Do Differently / Next Steps
- Try a genuine code-level vulnerability (not a planted backdoor) such as the Samba RCE also present on this target
- Practice identifying misconfigurations proactively during recon rather than only after Nmap labels them explicitly
