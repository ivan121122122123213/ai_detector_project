from pathlib import Path
import zipfile, shutil

root = Path("sample_project")
if root.exists():
    shutil.rmtree(root)
(root / "backend").mkdir(parents=True)
(root / "backup").mkdir()
(root / "logs").mkdir()
(root / "config").mkdir()
(root / "src").mkdir()

(root / "backend" / ".env").write_text("""DATABASE_URL=postgres://app:password@example.com:5432/prod
API_KEY=sk_test_1234567890abcdef
JWT_SECRET=supersecretjwtvalue
SMTP_PASSWORD=mail-password-demo
""", encoding="utf-8")
(root / "backup" / "users.sql").write_text("""INSERT INTO users VALUES (1, 'ivan@example.com', '@telegram_user');
INSERT INTO users VALUES (2, 'test@company.ru', '0x742d35Cc6634C0532925a3b844Bc454e4438f44e');
""", encoding="utf-8")
(root / "logs" / "auth.log").write_text("""2026-01-01 login ip=192.168.1.10 user=ivan@example.com domain=example.com
2026-01-02 login ip=10.0.0.5 user=test@company.ru
""", encoding="utf-8")
(root / "config" / "prod.json").write_text('{"client_secret":"abcd1234secretvalue", "domain":"api.example.com"}', encoding="utf-8")
(root / "src" / "app.py").write_text("print('hello')", encoding="utf-8")

zip_path = Path("sample_sensitive_project.zip")
if zip_path.exists():
    zip_path.unlink()
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
    for p in root.rglob("*"):
        if p.is_file():
            z.write(p, p.relative_to(root))
print(f"Created {zip_path}")
