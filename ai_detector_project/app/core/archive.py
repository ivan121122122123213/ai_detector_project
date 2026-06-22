import os, tarfile, zipfile, tempfile, shutil
from pathlib import Path
from contextlib import contextmanager

MAX_EXTRACTED_FILES = 25000
MAX_TOTAL_SIZE = 750 * 1024 * 1024

class ArchiveError(Exception):
    pass

def _safe_path(base: Path, target: Path) -> bool:
    try:
        target.resolve().relative_to(base.resolve())
        return True
    except ValueError:
        return False

def _check_limits(root: Path):
    count = 0
    total = 0
    for p in root.rglob("*"):
        if p.is_file():
            count += 1
            total += p.stat().st_size
            if count > MAX_EXTRACTED_FILES:
                raise ArchiveError("Too many files in archive")
            if total > MAX_TOTAL_SIZE:
                raise ArchiveError("Archive is too large after extraction")

def extract_archive(archive_path: str, dest: Path):
    source = Path(archive_path)
    suffixes = ''.join(source.suffixes).lower()
    dest.mkdir(parents=True, exist_ok=True)

    if source.suffix.lower() == ".zip":
        with zipfile.ZipFile(source) as z:
            for member in z.infolist():
                target = dest / member.filename
                if not _safe_path(dest, target):
                    raise ArchiveError("Unsafe zip path detected")
            z.extractall(dest)
    elif suffixes.endswith(".tar") or suffixes.endswith(".tar.gz") or suffixes.endswith(".tgz"):
        with tarfile.open(source) as t:
            for member in t.getmembers():
                target = dest / member.name
                if not _safe_path(dest, target):
                    raise ArchiveError("Unsafe tar path detected")
            t.extractall(dest)
    else:
        raise ArchiveError("Supported archives: .zip, .tar, .tar.gz, .tgz")

    _check_limits(dest)

@contextmanager
def extracted_archive(archive_path: str):
    tmp = Path(tempfile.mkdtemp(prefix="aidetector_"))
    try:
        extract_archive(archive_path, tmp)
        yield tmp
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

def build_tree(root: Path, max_nodes: int = 1500):
    nodes = 0
    def walk(path: Path):
        nonlocal nodes
        nodes += 1
        if nodes > max_nodes:
            return {"name": "...truncated", "type": "limit"}
        if path.is_dir():
            children = []
            try:
                items = sorted(path.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))[:80]
                children = [walk(item) for item in items]
            except Exception:
                children = []
            return {"name": path.name or "root", "type": "dir", "children": children}
        return {"name": path.name, "type": "file", "size": path.stat().st_size if path.exists() else 0}
    return walk(root)
