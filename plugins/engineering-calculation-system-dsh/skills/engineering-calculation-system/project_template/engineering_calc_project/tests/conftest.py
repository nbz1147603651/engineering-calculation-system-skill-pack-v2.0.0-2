import sys
import shutil
from pathlib import Path


sys.dont_write_bytecode = True


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC = PROJECT_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


def pytest_sessionfinish(session, exitstatus):
    for cache_dir in PROJECT_ROOT.rglob("__pycache__"):
        if cache_dir.is_dir():
            shutil.rmtree(cache_dir, ignore_errors=True)
    pytest_cache = PROJECT_ROOT / ".pytest_cache"
    if pytest_cache.exists():
        shutil.rmtree(pytest_cache, ignore_errors=True)
