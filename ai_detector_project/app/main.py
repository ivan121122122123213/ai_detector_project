from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import shutil

from .core.scanner import scan_archive_file
from .core.database import init_db, save_analysis, list_analyses, get_analysis
from .core.report import save_json, save_html, REPORT_DIR
from .core.archive import ArchiveError

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

app = FastAPI(title="AI Detector / Intelligence Dashboard", version="1.0.0")
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

@app.on_event("startup")
def startup():
    init_db()

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/analyses")
def analyses():
    return list_analyses()

@app.get("/api/analyses/{analysis_id}")
def analysis_detail(analysis_id: str):
    data = get_analysis(analysis_id)
    if not data:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return data

@app.post("/api/scan")
async def scan(file: UploadFile = File(...)):
    allowed = (".zip", ".tar", ".tar.gz", ".tgz")
    lower_name = file.filename.lower()
    if not lower_name.endswith(allowed):
        raise HTTPException(status_code=400, detail="Supported formats: zip, tar, tar.gz, tgz")

    safe_name = Path(file.filename).name
    saved_path = UPLOAD_DIR / safe_name
    with saved_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        report = scan_archive_file(str(saved_path), safe_name)
    except ArchiveError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scan failed: {e}")

    save_analysis(report)
    save_json(report)
    save_html(report)
    return report.model_dump()

@app.get("/api/search/{analysis_id}")
def search(analysis_id: str, q: str = ""):
    data = get_analysis(analysis_id)
    if not data:
        raise HTTPException(status_code=404, detail="Analysis not found")
    ql = q.lower().strip()
    if not ql:
        return []
    results = []
    for f in data.get("risky_files", []):
        hay = f.get("path", "").lower() + " " + f.get("classification", "").lower() + " " + " ".join(f.get("findings", {}).keys()).lower()
        if ql in hay:
            results.append(f)
    return results[:100]

@app.get("/reports/{analysis_id}.json")
def report_json(analysis_id: str):
    path = REPORT_DIR / f"{analysis_id}.json"
    if not path.exists():
        raise HTTPException(status_code=404, detail="Report not found")
    return FileResponse(str(path), media_type="application/json", filename=path.name)

@app.get("/reports/{analysis_id}.html")
def report_html(analysis_id: str):
    path = REPORT_DIR / f"{analysis_id}.html"
    if not path.exists():
        raise HTTPException(status_code=404, detail="Report not found")
    return FileResponse(str(path), media_type="text/html", filename=path.name)
