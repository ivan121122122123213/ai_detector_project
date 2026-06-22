from pathlib import Path

SOURCE_EXT = {".py", ".js", ".ts", ".tsx", ".jsx", ".php", ".go", ".java", ".rb", ".rs", ".c", ".cpp", ".cs"}
DB_EXT = {".sql", ".sqlite", ".db", ".mdb"}
LOG_EXT = {".log"}
SPREADSHEET_EXT = {".csv", ".xlsx", ".xls"}
CONFIG_NAMES = {".env", "docker-compose.yml", "docker-compose.yaml", "settings.py", "config.json", "prod.json", "production.json"}
CONFIG_EXT = {".env", ".ini", ".conf", ".yaml", ".yml", ".json", ".toml"}
BACKUP_HINTS = ["backup", "dump", "old", "copy", "bak"]
BROWSER_HINTS = ["cookie", "cookies", "history", "browser", "local storage", "session"]

def classify_file(path: Path) -> str:
    name = path.name.lower()
    suffix = path.suffix.lower()
    full = str(path).lower()
    if name in CONFIG_NAMES or suffix in CONFIG_EXT:
        return "Config Files"
    if suffix in DB_EXT:
        return "Databases"
    if suffix in LOG_EXT:
        return "Logs"
    if suffix in SOURCE_EXT:
        return "Source Code"
    if suffix in SPREADSHEET_EXT:
        return "Spreadsheets"
    if any(h in full for h in BACKUP_HINTS):
        return "Backups"
    if any(h in full for h in BROWSER_HINTS):
        return "Browser Data"
    return "Other"
