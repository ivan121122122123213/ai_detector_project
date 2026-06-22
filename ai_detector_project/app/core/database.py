import sqlite3, json
from pathlib import Path
from .models import AnalysisReport

DB_PATH = Path(__file__).resolve().parents[1] / "aidetector.sqlite3"

def init_db():
    with sqlite3.connect(DB_PATH) as con:
        con.execute("""
        CREATE TABLE IF NOT EXISTS analyses (
            id TEXT PRIMARY KEY,
            filename TEXT NOT NULL,
            risk_score INTEGER NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            payload TEXT NOT NULL
        )
        """)
        con.commit()

def save_analysis(report: AnalysisReport):
    with sqlite3.connect(DB_PATH) as con:
        con.execute(
            "INSERT OR REPLACE INTO analyses (id, filename, risk_score, payload) VALUES (?, ?, ?, ?)",
            (report.id, report.filename, report.risk_score, report.model_dump_json())
        )
        con.commit()

def list_analyses():
    with sqlite3.connect(DB_PATH) as con:
        con.row_factory = sqlite3.Row
        rows = con.execute("SELECT id, filename, risk_score, created_at FROM analyses ORDER BY created_at DESC LIMIT 50").fetchall()
        return [dict(r) for r in rows]

def get_analysis(analysis_id: str):
    with sqlite3.connect(DB_PATH) as con:
        row = con.execute("SELECT payload FROM analyses WHERE id=?", (analysis_id,)).fetchone()
        if not row:
            return None
        return json.loads(row[0])
