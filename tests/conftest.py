import pytest
from lean_interact import AutoLeanServer, LeanREPLConfig, LocalProject

from harness import config as cfg


@pytest.fixture(scope="session")
def lean_server():
    config = LeanREPLConfig(project=LocalProject(directory=str(cfg.LEAN_PROJECT_DIR)), verbose=False)
    # Dev machines are often near AutoLeanServer's default 80% system-memory guard from
    # unrelated apps; these tests don't import Mathlib, so actual usage stays low regardless.
    server = AutoLeanServer(config, max_total_memory=cfg.MAX_TOTAL_MEMORY)
    yield server
    server.kill()
