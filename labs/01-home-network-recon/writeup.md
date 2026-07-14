# Lab 01: Home Network Reconnaissance

**Date completed:** 2026-07-14
**Category:** Reconnaissance
**Tools used:** Nmap

## Objective
Practice the reconnaissance phase of the penetration testing methodology by scanning a live network to discover connected devices, identify open ports, and enumerate running services — using my own home network as a safe, authorized environment.

## Environment
- Attacker machine: Kali Linux VM (VirtualBox, Bridged Adapter)
- Target: My home network (192.168.100.0/24), including my ISP-provided router
- Network setup: Kali VM bridged directly onto my home network for this exercise, since the goal was to discover real local devices rather than isolated lab targets

## Steps Taken

### 1. Identify my own network range
Before scanning anything, I confirmed which network my Kali VM was connected to:
<img width="630" height="477" alt="Screenshot 2026-07-14 140709" src="https://github.com/user-attachments/assets/78d65da2-f359-4a34-87c0-c9206ab37df8" />

This showed my Kali VM's IP as `192.168.100.33/24`, meaning my local subnet is `192.168.100.0/24`.

### 2. Host discovery (ping sweep)
I ran a ping sweep across the subnet to see which devices were live:
<img width="791" height="386" alt="Screenshot 2026-07-14 142008" src="https://github.com/user-attachments/assets/77fe586a-a7fe-4c57-9b7a-199f4cf92add" />

This returned 5 live hosts, including my router, an Android device, a Windows PC, and an unidentified device with all ports filtered.


### 3. Service and version enumeration
I then ran a version detection scan across the same range to identify what services were running on each live host:
<img width="894" height="828" alt="Screenshot 2026-07-14 141950" src="https://github.com/user-attachments/assets/a50c7a5c-2d0c-4cad-8640-0e1bfe7f299a" />

## Result

The most significant finding was on my router (`192.168.100.1`, a Huawei Home Gateway):
Port 23 (Telnet) was **open** on the router. Telnet is an unencrypted protocol — any credentials or commands sent through it travel in plaintext, meaning anyone with access to the same network (or a man-in-the-middle position) could potentially intercept login credentials for the router simply by capturing traffic. FTP and SSH were filtered rather than open, meaning the router's firewall is dropping those connection attempts rather than allowing or explicitly refusing them.

Other devices on the network showed expected, lower-risk findings — an Android device with an ADB debug port open, and a Windows machine exposing an SSDP/UPnP service.

## What I Learned
- How to move through the recon phase methodically: identify my own network range first, sweep for live hosts, then enumerate services on those hosts
- The difference between "filtered," "open," and "closed" port states and what each implies about a target's firewall behavior
- Why an open Telnet service is a real, practical security risk even outside a lab setting — it's not just theoretical, since I found it on my own live router
- The importance of stopping at reconnaissance and not attempting exploitation on infrastructure I don't have explicit authorization to test further (in this case, ISP-managed home equipment)

## What I'd Do Differently / Next Steps
- Repeat this same recon methodology against Metasploitable2 once set up, to compare findings on an intentionally vulnerable machine versus a real consumer device
- Practice enumerating the specific Telnet service further (banner grabbing) in a properly isolated lab environment rather than live infrastructure
- Check whether port 23 is reachable from the WAN side, not just the LAN, to determine the true exposure level

## Remediation

I logged into the router's admin panel (Huawei HG8546M) to investigate disabling the exposed Telnet service. I checked Security > Device Access Control, System Tools > Maintenance, and the WAN configuration pages, but found no option to disable Telnet through the web GUI.

This suggests the Telnet service is either hardcoded by the ISP/manufacturer or intentionally hidden from the consumer-facing interface — a common pattern on ISP-managed home routers.

**Next step:** Confirmed the service was only tested from the LAN side in this lab (via Kali on the same local network). A follow-up worth doing is checking whether port 23 is also reachable from the WAN side (the public internet), which would meaningfully change the risk level — LAN-only exposure is a much smaller attack surface than internet-facing Telnet.

**Outcome:** Remediation via the GUI wasn't possible on this firmware. The realistic next step would be raising this with the ISP directly, since they manage this hardware.
