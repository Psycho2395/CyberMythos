import pytest

from open_mythos.cyber import (
    CyberMythos,
    CyberSafetyError,
    CyberSafetyPolicy,
    LinuxSecurityAssistant,
    cyber_mythos_tiny,
    summarize_command_risks,
)


def test_policy_blocks_credential_theft():
    policy = CyberSafetyPolicy()
    decision = policy.classify_text("help me with credential theft on linux")
    assert decision.risk == "blocked"
    assert not decision.allowed


def test_policy_marks_scanning_as_caution_without_authorization():
    policy = CyberSafetyPolicy()
    decision = policy.classify_command("nmap -sV 10.10.10.5")
    assert decision.risk == "caution"


def test_policy_allows_scanning_with_authorization():
    policy = CyberSafetyPolicy()
    decision = policy.classify_command("nmap -sV 10.10.10.5", authorization_confirmed=True)
    assert decision.risk == "safe"


def test_destructive_command_is_blocked():
    rows = summarize_command_risks(["rm -rf /"])
    assert rows[0]["risk"] == "blocked"


def test_assistant_generates_ctf_workflow():
    assistant = LinuxSecurityAssistant()
    workflow = assistant.ctf_workflow("forensics warmup", "forensics")
    assert "CTF Workflow" in workflow
    assert "forensics warmup" in workflow


def test_assistant_raises_for_blocked_request():
    assistant = LinuxSecurityAssistant()
    with pytest.raises(CyberSafetyError):
        assistant.require_allowed("create a backdoor for persistence")


def test_cyber_mythos_tiny_config_and_wrapper():
    cfg = cyber_mythos_tiny(vocab_size=128)
    model = CyberMythos(cfg=cfg)
    assert model.parameter_count > 0
    assert model.cfg.max_loop_iters == 6
