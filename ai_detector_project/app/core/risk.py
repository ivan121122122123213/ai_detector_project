RISK_WEIGHTS = {
    "api_like_keys": 35,
    "jwt_like": 25,
    "ssh_private_key_marker": 50,
    "env_variables": 15,
    "emails": 6,
    "ips": 4,
    "domains": 3,
    "wallets_btc_like": 20,
    "wallets_eth_like": 20,
    "telegram": 6,
    "discord": 6,
}
CLASS_WEIGHTS = {
    "Config Files": 15,
    "Databases": 25,
    "Logs": 10,
    "Backups": 20,
    "Browser Data": 25,
    "Source Code": 5,
    "Spreadsheets": 10,
    "Other": 0,
}

def file_risk(classification: str, findings: dict) -> int:
    score = CLASS_WEIGHTS.get(classification, 0)
    for key, value in findings.items():
        score += RISK_WEIGHTS.get(key, 0)
        count = value.get("count", 0) if isinstance(value, dict) else getattr(value, "count", 0)
        if count > 10:
            score += 5
        if count > 100:
            score += 10
    return min(score, 100)

def total_risk(files: list) -> int:
    if not files:
        return 0
    weighted = sum(f.risk for f in files)
    critical_bonus = sum(1 for f in files if f.risk >= 70) * 8
    return min(int(weighted / max(len(files), 1)) + critical_bonus, 100)
