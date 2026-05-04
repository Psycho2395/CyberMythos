"""CyberMythos: safety-scoped Linux security extension for OpenMythos.

This module adds a domain layer for authorized penetration testing labs, CTF
practice, bug-bounty methodology, Linux hardening, and defensive validation. It
intentionally does not execute offensive commands. Instead, it classifies task
risk and produces structured, scope-aware guidance.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable, Literal

from open_mythos.main import MythosConfig, OpenMythos

CyberMode = Literal[
    "ctf",
    "bug_bounty",
    "authorized_pentest",
    "linux_hardening",
    "defensive_validation",
]
RiskLevel = Literal["safe", "caution", "blocked"]


class CyberSafetyError(ValueError):
    """Raised when a requested workflow is outside the authorized-use boundary."""


@dataclass(frozen=True)
class SafetyDecision:
    """A structured safety decision for a prompt, command, or workflow."""

    risk: RiskLevel
    reason: str
    matched_terms: tuple[str, ...] = ()

    @property
    def allowed(self) -> bool:
        return self.risk != "blocked"


@dataclass
class CyberSafetyPolicy:
    """Simple transparent safety policy for Linux security assistance.

    The policy is deliberately conservative. It allows educational and defensive
    work, marks potentially intrusive security testing as requiring caution and
    explicit authorization, and blocks requests involving stealth, persistence,
    credential theft, destructive behavior, or unauthorized compromise.
    """

    blocked_terms: tuple[str, ...] = (
        "persistence",
        "evade detection",
        "bypass edr",
        "disable antivirus",
        "steal password",
        "credential theft",
        "token theft",
        "exfiltrate",
        "ransomware",
        "wipe logs",
        "cover tracks",
        "backdoor",
        "botnet",
        "keylogger",
        "phishing kit",
        "reverse shell",
        "privilege escalation exploit",
        "exploit public ip",
    )
    caution_terms: tuple[str, ...] = (
        "nmap",
        "masscan",
        "sqlmap",
        "metasploit",
        "hydra",
        "ffuf",
        "gobuster",
        "nikto",
        "burp",
        "exploit",
        "payload",
        "scan",
        "fuzz",
        "bruteforce",
        "brute force",
    )
    safe_terms: tuple[str, ...] = (
        "ctf",
        "lab",
        "authorized",
        "owned system",
        "bug bounty scope",
        "defensive",
        "hardening",
        "report",
        "triage",
        "logs",
    )

    def classify_text(self, text: str, authorization_confirmed: bool = False) -> SafetyDecision:
        """Classify natural-language task text under the safety policy."""

        lowered = text.lower()
        blocked = tuple(term for term in self.blocked_terms if term in lowered)
        if blocked:
            return SafetyDecision(
                risk="blocked",
                reason="The request contains terms associated with unauthorized compromise, stealth, credential theft, or destructive activity.",
                matched_terms=blocked,
            )

        caution = tuple(term for term in self.caution_terms if term in lowered)
        if caution and not authorization_confirmed:
            return SafetyDecision(
                risk="caution",
                reason="The request may be legitimate only in an explicitly authorized lab, CTF, internal test, or bug-bounty scope.",
                matched_terms=caution,
            )

        return SafetyDecision(
            risk="safe",
            reason="The request fits educational, defensive, reporting, or explicitly authorized security assistance.",
        )

    def classify_command(self, command: str, authorization_confirmed: bool = False) -> SafetyDecision:
        """Classify a Linux command before it is suggested or run elsewhere."""

        lowered = command.lower().strip()
        destructive_markers = (
            "rm -rf /",
            "mkfs",
            "dd if=",
            ":(){ :|:& };:",
            "chmod -r 777 /",
            "chown -r",
            "iptables -f",
            "history -c",
            "/etc/shadow",
            "ssh-keygen -f /root",
            "nc -e",
            "bash -i >&",
        )
        blocked = tuple(term for term in destructive_markers if term in lowered)
        if blocked:
            return SafetyDecision(
                risk="blocked",
                reason="The command appears destructive, stealthy, credential-oriented, or unsafe for general guidance.",
                matched_terms=blocked,
            )
        return self.classify_text(command, authorization_confirmed=authorization_confirmed)


@dataclass
class LinuxSecurityAssistant:
    """Scope-aware helper for Linux pentest, CTF, and bug-bounty workflows."""

    mode: CyberMode = "ctf"
    policy: CyberSafetyPolicy = field(default_factory=CyberSafetyPolicy)

    def require_allowed(self, text: str, authorization_confirmed: bool = False) -> SafetyDecision:
        """Return a decision or raise for blocked requests."""

        decision = self.policy.classify_text(text, authorization_confirmed)
        if decision.risk == "blocked":
            raise CyberSafetyError(decision.reason)
        return decision

    def classify_command(self, command: str, authorization_confirmed: bool = False) -> SafetyDecision:
        """Classify one Linux command according to the configured safety policy."""

        return self.policy.classify_command(command, authorization_confirmed)

    def authorized_recon_plan(self, target_description: str) -> str:
        """Create a non-destructive reconnaissance plan for an authorized target."""

        self.require_allowed(target_description, authorization_confirmed=True)
        return f"""# Authorized Reconnaissance Plan\n\nTarget scope: {target_description}\n\n1. Confirm the written scope, testing window, rate limits, and excluded systems before touching the target.\n2. Create a local evidence folder with timestamps, tool versions, and notes.\n3. Start with passive review: documentation, DNS records, public metadata, application routes, and known technology fingerprints.\n4. Use low-rate active checks only where permitted. Record exact commands, timestamps, and responses.\n5. Triage findings by reproducibility, impact, affected asset, preconditions, and remediation path.\n6. Stop immediately if testing produces instability, sensitive data exposure, or evidence that the target is outside scope.\n"""

    def ctf_workflow(self, challenge_name: str, category: str = "general") -> str:
        """Create a CTF-safe workflow without revealing weaponized real-target tactics."""

        return f"""# CTF Workflow: {challenge_name}\n\nCategory: {category}\n\n1. Read the challenge statement carefully and list all supplied files, services, credentials, and constraints.\n2. Establish a reproducible workspace: capture hashes, file types, strings, metadata, and runtime environment details.\n3. Enumerate gently inside the lab boundary. Prefer observation, source review, protocol inspection, and hypothesis-driven tests.\n4. Keep a solution log with commands, expected outputs, surprising artifacts, and failed hypotheses.\n5. Convert each observation into a testable hypothesis, then validate the simplest hypothesis first.\n6. When solved, write a clean explanation: vulnerability class, root cause, exploit path inside the lab, and defensive lesson.\n"""

    def linux_hardening_checklist(self) -> str:
        """Return a practical Linux defensive checklist."""

        return """# Linux Hardening Checklist\n\n| Area | Checks | Evidence |\n| --- | --- | --- |\n| Identity | Review local users, sudoers, SSH keys, password policy, and inactive accounts. | `/etc/passwd`, `/etc/sudoers`, SSH authorized keys, PAM config. |\n| Network | List listening services, firewall rules, DNS settings, and exposed management ports. | `ss -tulpen`, firewall status, service inventory. |\n| Patching | Verify OS release, kernel version, package update status, and reboot requirements. | OS metadata, package manager output, kernel version. |\n| Services | Disable unnecessary daemons and confirm secure service configuration. | system service inventory and config diffs. |\n| Logging | Confirm audit, auth, system, and application logs are retained and monitored. | log configuration and sample events. |\n| Filesystems | Review mount options, sensitive permissions, world-writable paths, and backups. | mount table, permission scan, backup policy. |\n"""

    def bug_bounty_report(
        self,
        title: str,
        asset: str,
        severity: str,
        summary: str,
        impact: str,
        remediation: str,
    ) -> str:
        """Generate a professional bug-bounty report skeleton."""

        return f"""# {title}\n\n| Field | Value |\n| --- | --- |\n| Asset | {asset} |\n| Severity | {severity} |\n| Status | Draft |\n\n## Summary\n\n{summary}\n\n## Impact\n\n{impact}\n\n## Reproduction Notes\n\nDocument only actions performed within the authorized program scope. Include timestamps, accounts used, request IDs, affected endpoints, screenshots, and minimal proof-of-concept evidence sufficient for validation. Avoid including secrets, personal data, or excessive data extraction.\n\n## Remediation\n\n{remediation}\n\n## Responsible Testing Statement\n\nTesting was limited to the declared scope and stopped before causing service disruption, persistence, lateral movement, or exposure of unrelated data.\n"""


def cyber_mythos_tiny(vocab_size: int = 32000) -> MythosConfig:
    """Return a tiny CyberMythos configuration suitable for CPU smoke tests."""

    return MythosConfig(
        vocab_size=vocab_size,
        dim=128,
        n_heads=4,
        n_kv_heads=2,
        max_seq_len=512,
        max_loop_iters=6,
        prelude_layers=1,
        coda_layers=1,
        n_experts=4,
        n_shared_experts=1,
        n_experts_per_tok=2,
        expert_dim=64,
        lora_rank=4,
        attn_type="gqa",
        max_output_tokens=256,
        dropout=0.0,
    )


def cyber_mythos_1b(vocab_size: int = 32000) -> MythosConfig:
    """Return a research-scale CyberMythos 1B-style configuration."""

    return MythosConfig(
        vocab_size=vocab_size,
        dim=2048,
        n_heads=16,
        n_kv_heads=4,
        max_seq_len=8192,
        max_loop_iters=24,
        prelude_layers=2,
        coda_layers=2,
        n_experts=64,
        n_shared_experts=2,
        n_experts_per_tok=4,
        expert_dim=2048,
        lora_rank=16,
        attn_type="gqa",
        max_output_tokens=4096,
        dropout=0.05,
    )


@dataclass
class CyberMythos:
    """Convenience wrapper combining an OpenMythos model and Linux security helpers."""

    cfg: MythosConfig = field(default_factory=cyber_mythos_tiny)
    mode: CyberMode = "ctf"

    def __post_init__(self) -> None:
        self.model = OpenMythos(self.cfg)
        self.assistant = LinuxSecurityAssistant(mode=self.mode)

    @property
    def parameter_count(self) -> int:
        """Return the number of trainable and tied parameters reported by PyTorch."""

        return sum(p.numel() for p in self.model.parameters())

    def safe_prompt_header(self, task: str, authorization_confirmed: bool = False) -> str:
        """Create a system-style prompt prefix after safety classification."""

        decision = self.assistant.require_allowed(task, authorization_confirmed)
        return (
            "You are CyberMythos, an AI assistant for authorized Linux security work. "
            "Stay within declared scope, prefer defensive and educational guidance, "
            "avoid stealth, credential theft, persistence, or destructive activity, and "
            f"treat this task as {decision.risk}: {decision.reason}"
        )


def summarize_command_risks(commands: Iterable[str], authorization_confirmed: bool = False) -> list[dict[str, str]]:
    """Classify several commands and return serializable risk records."""

    policy = CyberSafetyPolicy()
    rows: list[dict[str, str]] = []
    for command in commands:
        decision = policy.classify_command(command, authorization_confirmed)
        rows.append(
            {
                "command": command,
                "risk": decision.risk,
                "reason": decision.reason,
                "matched_terms": ", ".join(decision.matched_terms),
            }
        )
    return rows
