import json
import subprocess
import sys
from pathlib import Path

from fastapi import APIRouter, BackgroundTasks
from fastapi.responses import JSONResponse

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parents[2]
REPORT_FILE = BASE_DIR / "test_report.json"


def run_pytest_proccess():
    """Запускает pytest в отдельном Python-процессе."""
    if REPORT_FILE.exists():
        REPORT_FILE.unlink()

    subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "tests/",
            "--json-report",
            f"--json-report-file={REPORT_FILE.name}",
        ],
        cwd=str(BASE_DIR),
        check=False,
    )


@router.post("/run-tests")
async def start_tests(background_tasks: BackgroundTasks):
    """Запускает тесты на фоне."""
    background_tasks.add_task(run_pytest_proccess)

    return {
        "status": "Тесты запущены в фоне",
        "msg": "Отправьте GET запрос на /test-results через несколько секунд, чтобы получить конфигурацию и результат."
    }


@router.get("/test-results")
async def get_test_results():
    if not REPORT_FILE.exists():
        return JSONResponse(
            status_code=202,
            content={"status": "Тесты все еще выполняются или еще не запускались"}
        )

    with REPORT_FILE.open("r", encoding="utf-8") as f:
        report_data = json.load(f)

    return {
        "status": "Выполнено",
        "summary": report_data.get("summary"),
        "tests": report_data.get("tests")
    }