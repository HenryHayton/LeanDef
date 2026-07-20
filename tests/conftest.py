from pathlib import Path

import pytest
from lean_interact import AutoLeanServer, LeanREPLConfig, LocalProject

LEAN_PROJECT_DIR = Path(__file__).resolve().parent.parent / "lean"


@pytest.fixture(scope="session")
def lean_server():
    config = LeanREPLConfig(project=LocalProject(directory=str(LEAN_PROJECT_DIR)), verbose=False)
    # Dev machines are often near AutoLeanServer's default 80% system-memory guard from
    # unrelated apps; these tests don't import Mathlib, so actual usage stays low regardless.
    server = AutoLeanServer(config, max_total_memory=0.95)
    yield server
    server.kill()
