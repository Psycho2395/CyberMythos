# CyberMythos Design

CyberMythos is a safety-scoped extension of OpenMythos for **authorized Linux security work**, CTF training, lab-based penetration testing, and bug-bounty research. It uses OpenMythos as the recurrent-depth language-model backbone and adds domain-specific configuration, task routing, Linux command guidance, reporting helpers, and a refusal-aware safety layer.

> CyberMythos is intended only for systems that the operator owns, administers, or has explicit permission to test. It must not be used for unauthorized access, stealth, persistence, credential theft, exploitation of third-party targets, or destructive activity.

## Architectural Overview

The repository already provides a recurrent-depth transformer backbone with prelude blocks, a recurrent block, and coda blocks. CyberMythos keeps that neural architecture intact and adds an application layer that prepares prompts, validates workflows, and structures outputs for security use cases.

| Layer | Purpose | Implementation |
| --- | --- | --- |
| Model backbone | Recurrent-depth reasoning over security tasks | `OpenMythos` with CyberMythos model presets |
| Domain configuration | Small, medium, and research-scale security model configs | `open_mythos/cyber.py` |
| Safety policy | Scope enforcement and command risk classification | `CyberSafetyPolicy` |
| Linux workflow tools | Authorized recon, CTF enumeration, web testing guidance, and reporting templates | `LinuxSecurityAssistant` |
| Training preparation | Supervised fine-tuning examples with safe labels and refusal examples | `training/cyber_finetune_blueprint.py` |
| CLI entry point | Local Linux helper for safe planning and report generation | `examples/cyber_mythos_cli.py` |

## Safety Boundary

CyberMythos may provide high-level methodology, lab-safe CTF guidance, defensive validation steps, and report-writing assistance. It must refuse or redirect requests that ask for real-world exploitation without authorization, stealth, persistence, malware, credential theft, destructive commands, or post-compromise operations.

| Allowed | Disallowed |
| --- | --- |
| CTF lab enumeration and hints | Exploiting public IPs without written authorization |
| Bug-bounty methodology within declared scope | Credential theft, phishing, token harvesting, password spraying |
| Defensive vulnerability validation | Persistence, evasion, destructive wiping, ransomware behavior |
| Linux hardening and secure configuration | Stealthy intrusion, lateral movement, or exfiltration |
| Professional vulnerability reports | Instructions to bypass detection or accountability |

## Advanced Linux Features

CyberMythos focuses on safe Linux workflows that are useful in legitimate security operations. The first implementation includes scope-aware command classification, CTF checklist generation, bug-bounty report drafting, authorized recon planning, log-review prompts, and Linux hardening advice. Commands are marked as `safe`, `caution`, or `blocked`; blocked actions are not executed or recommended.

## Training Strategy

The model should be trained or fine-tuned only on authorized and educational datasets. Recommended sources include CTF writeups with permission-compatible licenses, intentionally vulnerable lab documentation, CVE descriptions, CWE/CAPEC text, defensive advisories, secure coding guides, and synthetic refusal examples. The blueprint script writes JSONL examples that can be adapted for supervised fine-tuning.

## Practical Limitations

This implementation creates the code and scaffolding for a CyberMythos model family. Training a useful security LLM requires significant compute, curated datasets, evaluation harnesses, and safety review. The included code can instantiate tiny test models locally and can prepare data formats, but it does not ship pretrained security weights.
