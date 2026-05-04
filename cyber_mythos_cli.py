"""CyberMythos command-line helper for authorized Linux security workflows.

Examples:
    python examples/cyber_mythos_cli.py classify "nmap -sV 10.10.10.5"
    python examples/cyber_mythos_cli.py ctf --name "web warmup" --category web
    python examples/cyber_mythos_cli.py hardening
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from open_mythos.cyber import (  # noqa: E402
    CyberMythos,
    LinuxSecurityAssistant,
    summarize_command_risks,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="CyberMythos Linux security helper")
    sub = parser.add_subparsers(dest="command", required=True)

    classify = sub.add_parser("classify", help="Classify command risk")
    classify.add_argument("commands", nargs="+", help="Command strings to classify")
    classify.add_argument("--authorized", action="store_true", help="Confirm the command is for an authorized target or lab")
    classify.add_argument("--json", action="store_true", help="Print machine-readable JSON")

    ctf = sub.add_parser("ctf", help="Create a CTF workflow")
    ctf.add_argument("--name", required=True, help="Challenge name")
    ctf.add_argument("--category", default="general", help="Challenge category")

    recon = sub.add_parser("recon", help="Create an authorized reconnaissance plan")
    recon.add_argument("--scope", required=True, help="Written target scope description")

    report = sub.add_parser("report", help="Create a bug-bounty report skeleton")
    report.add_argument("--title", required=True)
    report.add_argument("--asset", required=True)
    report.add_argument("--severity", default="Informational")
    report.add_argument("--summary", required=True)
    report.add_argument("--impact", required=True)
    report.add_argument("--remediation", required=True)

    sub.add_parser("hardening", help="Print a Linux hardening checklist")
    sub.add_parser("model-info", help="Instantiate the tiny CyberMythos model and print parameter count")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    assistant = LinuxSecurityAssistant()

    if args.command == "classify":
        rows = summarize_command_risks(args.commands, authorization_confirmed=args.authorized)
        if args.json:
            print(json.dumps(rows, indent=2))
        else:
            for row in rows:
                print(f"[{row['risk']}] {row['command']} — {row['reason']}")
        return

    if args.command == "ctf":
        print(assistant.ctf_workflow(args.name, args.category))
        return

    if args.command == "recon":
        print(assistant.authorized_recon_plan(args.scope))
        return

    if args.command == "report":
        print(
            assistant.bug_bounty_report(
                title=args.title,
                asset=args.asset,
                severity=args.severity,
                summary=args.summary,
                impact=args.impact,
                remediation=args.remediation,
            )
        )
        return

    if args.command == "hardening":
        print(assistant.linux_hardening_checklist())
        return

    if args.command == "model-info":
        model = CyberMythos()
        print(f"CyberMythos tiny parameters: {model.parameter_count:,}")
        print(f"Max loops: {model.cfg.max_loop_iters}; context: {model.cfg.max_seq_len}")
        return


if __name__ == "__main__":
    main()
