# Acme AeroTech — Network Vulnerability & Resilience Assessment


*Capstone Project 1 — Moringa School, Cybersecurity Program (Group Project)*

This project was completed as a group effort. System analysis and vulnerability identification were carried out collaboratively by the whole team; the network diagram was drawn together with a colleague.


## Scenario

Acme AeroTech is a mid-sized U.S. aerospace parts manufacturer specializing in lightweight components for commercial aircraft. The company has 75 employees, supported by a two-person internal IT team.

Acme recently won a government contract that requires an improved cybersecurity posture and more reliable network availability. This assessment is the company's first third-party security and resilience review.

## Environment

The current network was built five years ago and has not been updated since. Due to limited IT staff and budget, it was built with minimal redundancy:

- Flat topology — every device shares a single subnet, with no segmentation between servers, workstations, and IoT devices
- Default credentials in use on the router, web server, FTP server, and database
- No patch management program
- No DMZ — internet-facing services (web, FTP) sit on the same network as internal systems
- Single firewall, switch, and router/ISP link — the company has already experienced intermittent outages, including full loss of internal access during firewall and switch maintenance

## Objective

Acting as a cybersecurity analyst, the goal is to:

1. Identify security vulnerabilities and availability risks in the current architecture
2. Assess their impact on operations
3. Design an improved network — segmented, redundant, and monitored — that a two-person IT team can realistically operate
4. Recommend controls, prioritized by risk and by cost/complexity/user impact

## Constraints

Every design decision had to hold up against one question: **can two people actually run this day to day?** That ruled out some "textbook ideal" options (e.g. full active/active HA everywhere, per-device NAC) in favor of scoped, risk-prioritized alternatives — cloud-managed tooling, a single jump server for admin access, and redundancy focused on the components that had already caused outages.

## Deliverables

- Vulnerability analysis and risk prioritization
- Redesigned network diagram (segmented VLANs, DMZ, redundant core, centralized logging)
- Written report: findings, design rationale, and recommendations
- Slide deck and video walkthrough

---

*Capstone Project 1 — Moringa School, Cybersecurity Program*

## Initial Network
![Initial network diagram](initial-network-diagram.png)

## Redesigned Network
![Redesigned network diagram](redesigned-network-diagram.jpeg)
