import pytest
from open_mythos.cyber import CyberMythos

def test_offsec_recon_skill():
    model = CyberMythos()
    strategy = model.recon.suggest_recon_strategy("example.com")
    assert "example.com" in strategy
    assert "passive reconnaissance" in strategy

def test_offsec_exploit_skill():
    model = CyberMythos()
    analysis = model.exploit.analyze_vulnerability("buffer overflow")
    assert "buffer overflow" in analysis
    assert "Exploit-DB" in analysis

def test_offsec_privesc_skill():
    model = CyberMythos()
    analysis = model.privesc.analyze_enumeration_output("linpeas output", os_type="linux")
    assert "linux" in analysis
    assert "SUID binary" in analysis

def test_offsec_web_skill():
    model = CyberMythos()
    analysis = model.web.analyze_web_vulnerability("SQL injection", "search page")
    assert "SQL injection" in analysis
    assert "search page" in analysis

def test_offsec_ad_skill():
    model = CyberMythos()
    analysis = model.ad.analyze_ad_data("bloodhound data")
    assert "AS-REP Roasting" in analysis
