import re

PATTERNS = {
    "emails": re.compile(r"\b[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+\b"),
    "ips": re.compile(r"\b(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)\b"),
    "domains": re.compile(r"\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b"),
    "telegram": re.compile(r"(?i)(?:t\.me/|telegram\.me/|@)[a-zA-Z0-9_]{5,32}"),
    "discord": re.compile(r"(?i)(?:discord\.gg/[a-zA-Z0-9]+|discord(?:app)?\.com/invite/[a-zA-Z0-9]+)"),
    "wallets_btc_like": re.compile(r"\b(?:bc1|[13])[a-zA-HJ-NP-Z0-9]{25,62}\b"),
    "wallets_eth_like": re.compile(r"\b0x[a-fA-F0-9]{40}\b"),
    "jwt_like": re.compile(r"\beyJ[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}\b"),
    "api_like_keys": re.compile(r"(?i)\b(?:api[_-]?key|secret|access[_-]?token|auth[_-]?token|client[_-]?secret|jwt[_-]?secret|smtp[_-]?password|database[_-]?url)\s*[:=]\s*[\"']?([^\s\"'<>]{8,})"),
    "ssh_private_key_marker": re.compile(r"-----BEGIN (?:RSA |OPENSSH |DSA |EC |)PRIVATE KEY-----"),
    "env_variables": re.compile(r"(?m)^\s*[A-Z0-9_]{3,64}\s*=\s*.+$"),
}

TEXT_EXTENSIONS = {
    ".txt", ".log", ".csv", ".json", ".xml", ".yaml", ".yml", ".env", ".ini", ".conf",
    ".py", ".js", ".ts", ".tsx", ".jsx", ".php", ".go", ".java", ".rb", ".rs", ".sql",
    ".md", ".html", ".css", ".sh", ".bat", ".ps1"
}
