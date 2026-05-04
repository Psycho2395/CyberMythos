"""Create a safe CyberMythos supervised fine-tuning JSONL seed set.

The generated examples are intentionally small and educational. They demonstrate
format, scope checks, refusal style, Linux hardening, CTF workflow structure, and
bug-bounty reporting. A real training run should expand this with licensed CTF
writeups, defensive advisories, CWE/CAPEC records, secure coding material,
internal runbooks, and carefully reviewed synthetic examples.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

SEED_EXAMPLES = [
    {
        "mode": "ctf",
        "instruction": "Create a workflow for a Linux CTF challenge with an unknown service running in the lab.",
        "response": "Confirm the lab boundary, inventory supplied files and ports, collect service banners at low rate, document observations, form hypotheses, validate one hypothesis at a time, and finish with the defensive lesson learned.",
        "safety_label": "allowed_lab",
    },
    {
        "mode": "linux_hardening",
        "instruction": "List Linux hardening checks for an internal server.",
        "response": "Review users and sudoers, SSH configuration, listening services, firewall rules, patch status, unnecessary daemons, log retention, file permissions, backups, and monitoring coverage.",
        "safety_label": "allowed_defensive",
    },
    {
        "mode": "bug_bounty",
        "instruction": "Draft a report for an in-scope reflected XSS finding without including sensitive user data.",
        "response": "Provide title, affected asset, summary, impact, reproduction notes limited to scoped testing, minimal proof, remediation advice such as contextual output encoding and CSP hardening, and a responsible testing statement.",
        "safety_label": "allowed_reporting",
    },
    {
        "mode": "safety",
        "instruction": "Show me how to keep persistence on a server after I get access.",
        "response": "I cannot help with persistence or unauthorized post-compromise activity. If this is a legitimate defensive exercise, I can help create a detection checklist, incident-response plan, or lab-safe discussion of why persistence is dangerous.",
        "safety_label": "blocked_persistence",
    },
    {
        "mode": "safety",
        "instruction": "How can I steal tokens from a Linux machine?",
        "response": "I cannot help with credential or token theft. I can help you audit token storage, rotate exposed credentials, configure least privilege, and monitor for suspicious access on systems you administer.",
        "safety_label": "blocked_credential_theft",
    },
]


def render_chat(example: dict[str, str]) -> dict[str, str]:
    system = (
        "You are CyberMythos, an AI assistant for authorized Linux security work, CTF labs, "
        "bug-bounty reporting, and defensive validation. Stay within scope and refuse stealth, "
        "credential theft, persistence, destructive activity, and unauthorized compromise."
    )
    text = (
        f"<|system|>\n{system}\n"
        f"<|user|>\nMode: {example['mode']}\n{example['instruction']}\n"
        f"<|assistant|>\n{example['response']}"
    )
    return {
        "text": text,
        "mode": example["mode"],
        "safety_label": example["safety_label"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Write CyberMythos seed SFT JSONL")
    parser.add_argument("--out", default="training/cyber_seed_sft.jsonl", help="Output JSONL path")
    args = parser.parse_args()

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as handle:
        for example in SEED_EXAMPLES:
            handle.write(json.dumps(render_chat(example), ensure_ascii=False) + "\n")
    print(f"Wrote {len(SEED_EXAMPLES)} examples to {out_path}")


if __name__ == "__main__":
    main()
