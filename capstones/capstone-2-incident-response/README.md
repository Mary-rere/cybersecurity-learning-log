# Capstone 2: Incident Response Investigation

**Scenario:** Full incident response investigation for a fictional organization.

**Frameworks:** MITRE ATT&CK mapping, IoC catalogue.

**Team project:** Group project. Each member investigated the incident independently and produced their own findings.

**My contribution:** Completed my own investigation, including MITRE ATT&CK mapping and IoC cataloguing. Worked on the group pitch deck and delivered the presentation.

# HealthSecure Systems: Incident Response Report

Incident response investigation of a simulated phishing-driven breach at a healthcare software provider. Completed as a group capstone at Moringa School (Group 5).

## Scenario
HealthSecure Systems (HSS) provides EHR software to 50+ clinics. On April 12, 2025, its IDS flagged suspicious activity from a Finance workstation. I analyzed Windows Event Logs, Zeek, Snort, EDR data, a phishing email, an asset inventory, and honeypot data to reconstruct the attack and recommend a response.

## Key Findings
- **Entry point:** Spoofed HR-Payroll phishing email sent the night before.
- **Confirmed compromise:** Workstation-23 (Finance). PsExec service installed, obfuscated PowerShell payload downloaded, outbound connection to a malicious IP (corroborated by Zeek and Snort).
- **Attempted, not confirmed:** SMB/RDP to HR-SQL01 (payroll/PII) and SSH to DevAppServer (source code). Connections were logged, but no evidence of successful authentication.
- **Root cause:** Phishing plus a failed offboarding process. A former developer's account stayed active and his credentials were cached on the workstation.
- **Detection gaps:** No centralized SIEM, PowerShell logging disabled on ~30% of endpoints, no EDR alert on the Linux/DMZ SSH attempt (caught only by the honeypot).
- **Severity:** High.

## Method
Every claim is labeled confirmed, attempted, or unconfirmed. A network connection is never treated as compromise without evidence of authentication or action inside the session.

## Response Plan
- **Containment:** isolate host, block malicious IP/domains, disable stale accounts, reset credentials
- **Eradication:** re-image, remove payload, audit AD for other stale accounts
- **Recovery:** verified restoration, segmentation pen test, 90-day threat hunt
- **Long-term:** automated offboarding, SIEM, MFA, Linux/DMZ EDR parity, phishing simulations

## Deliverables
- [Incident Response Report](ir_report.pdf)
- [Presentation](pitch_deck.pptx)

## Skills Demonstrated
Log correlation (Snort, Zeek, Windows Event Logs), IoC extraction, timeline reconstruction, MITRE ATT&CK mapping, NIST-style IR lifecycle, evidence-based reporting, business-impact communication.

## Note
Fictional scenario provided by the course. No real organization or data.

