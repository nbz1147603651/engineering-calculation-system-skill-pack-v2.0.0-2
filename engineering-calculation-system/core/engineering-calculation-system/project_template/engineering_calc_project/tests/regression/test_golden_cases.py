from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.verify_golden_cases import run_golden_cases  # noqa: E402


def test_registered_golden_cases_match_run_book():
    results = run_golden_cases(PROJECT_ROOT)

    assert results
    failures = [result for result in results if result.status == "fail"]
    assert failures == []
    assert any(result.case_id == "GC001" and result.status == "pass" for result in results)
