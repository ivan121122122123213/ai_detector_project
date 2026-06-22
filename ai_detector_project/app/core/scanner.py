from pathlib import Path
from collections import Counter
from .patterns import PATTERNS, TEXT_EXTENSIONS
from .classifier import classify_file
from .risk import file_risk, total_risk
from .archive import extracted_archive, build_tree
from .models import Finding, FileResult, AnalysisReport
from .summary import build_summary
from .graph import build_graph
import uuid

MAX_READ_BYTES = 2_000_000
MAX_SAMPLES = 10

def mask(value: str) -> str:
    value = str(value).strip()
    if len(value) <= 6:
        return "***"
    if len(value) <= 12:
        return value[:2] + "***" + value[-2:]
    return value[:4] + "***" + value[-4:]

def read_text(path: Path) -> str:
    try:
        with path.open("rb") as f:
            data = f.read(MAX_READ_BYTES)
        return data.decode("utf-8", errors="ignore")
    except Exception:
        return ""

def scan_file(path: Path, root: Path) -> FileResult | None:
    rel = str(path.relative_to(root))
    suffix = path.suffix.lower()
    classification = classify_file(path)
    findings = {}

    should_read = suffix in TEXT_EXTENSIONS or path.name.lower() == ".env" or classification in {"Config Files", "Logs", "Source Code", "Databases", "Spreadsheets", "Browser Data"}
    if should_read:
        text = read_text(path)
        for name, regex in PATTERNS.items():
            matches = regex.findall(text)
            if matches:
                flat = []
                for m in matches[:MAX_SAMPLES]:
                    if isinstance(m, tuple):
                        m = " ".join([x for x in m if x])
                    flat.append(mask(str(m)))
                findings[name] = Finding(type=name, count=len(matches), samples=flat)

    if not findings and classification == "Other":
        return None

    risk = file_risk(classification, {k: v.model_dump() for k, v in findings.items()})
    return FileResult(path=rel, size=path.stat().st_size, extension=suffix or "none", classification=classification, risk=risk, findings=findings)

def scan_archive_file(archive_path: str, original_filename: str) -> AnalysisReport:
    analysis_id = str(uuid.uuid4())[:8]
    risky_files = []
    classifications = Counter()
    summary = Counter()
    files_total = 0
    files_scanned = 0

    with extracted_archive(archive_path) as root:
        tree = build_tree(root)
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            files_total += 1
            classification = classify_file(path)
            classifications[classification] += 1
            result = scan_file(path, root)
            if result:
                files_scanned += 1
                if result.findings or result.risk > 20:
                    risky_files.append(result)
                    for key, finding in result.findings.items():
                        summary[key] += finding.count

    risky_files = sorted(risky_files, key=lambda x: x.risk, reverse=True)[:300]
    score = total_risk(risky_files)
    graph = build_graph(risky_files)
    ai_summary = build_summary(score, summary, classifications, risky_files)
    return AnalysisReport(
        id=analysis_id,
        filename=original_filename,
        files_total=files_total,
        files_scanned=files_scanned,
        risk_score=score,
        summary=dict(summary),
        classifications=dict(classifications),
        risky_files=risky_files,
        tree=tree,
        graph=graph,
        ai_summary=ai_summary,
    )
