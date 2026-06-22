from pydantic import BaseModel
from typing import Dict, List, Optional

class Finding(BaseModel):
    type: str
    count: int
    samples: List[str]

class FileResult(BaseModel):
    path: str
    size: int
    extension: str
    classification: str
    risk: int
    findings: Dict[str, Finding]

class AnalysisReport(BaseModel):
    id: str
    filename: str
    files_total: int
    files_scanned: int
    risk_score: int
    summary: Dict[str, int]
    classifications: Dict[str, int]
    risky_files: List[FileResult]
    tree: Dict
    graph: Dict
    ai_summary: str
