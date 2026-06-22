import json, html
from pathlib import Path
from .models import AnalysisReport

REPORT_DIR = Path(__file__).resolve().parents[1] / "reports"
REPORT_DIR.mkdir(exist_ok=True)

def save_json(report: AnalysisReport) -> Path:
    path = REPORT_DIR / f"{report.id}.json"
    path.write_text(report.model_dump_json(indent=2), encoding="utf-8")
    return path

def save_html(report: AnalysisReport) -> Path:
    rows = []
    for f in report.risky_files[:100]:
        findings = ", ".join([f"{k}: {v.count}" for k, v in f.findings.items()])
        rows.append(f"<tr><td>{html.escape(f.path)}</td><td>{f.risk}</td><td>{html.escape(f.classification)}</td><td>{html.escape(findings)}</td></tr>")
    content = f"""
    <!doctype html><html><head><meta charset='utf-8'><title>AI Detector Report</title>
    <style>body{{font-family:Arial;background:#101215;color:#eee;padding:32px}}table{{width:100%;border-collapse:collapse}}td,th{{border-bottom:1px solid #333;padding:10px;text-align:left}}.score{{font-size:40px;font-weight:700}}</style></head>
    <body><h1>AI Detector Report</h1><p>{html.escape(report.filename)}</p><div class='score'>Risk Score: {report.risk_score}/100</div><p>{html.escape(report.ai_summary)}</p>
    <h2>Summary</h2><pre>{html.escape(json.dumps(report.summary, ensure_ascii=False, indent=2))}</pre>
    <h2>Risky files</h2><table><tr><th>Path</th><th>Risk</th><th>Class</th><th>Findings</th></tr>{''.join(rows)}</table></body></html>
    """
    path = REPORT_DIR / f"{report.id}.html"
    path.write_text(content, encoding="utf-8")
    return path
