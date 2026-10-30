import json
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

EXAMPLES = Path(__file__).parents[1] / "examples"


@pytest.fixture
def fresh_runner_snapshot(tmp_path):
    """Copy an example runner snapshot with snapshot_at set to one day ago.

    The shipped examples carry a fixed snapshot_at, and runner review treats a snapshot
    older than 30 days as stale. Tests that drive the CLI on the wall clock (in process or
    through the installed script) must not read the examples directly, or they start
    failing 30 days after the examples were written.
    """

    def make(name):
        raw = json.loads((EXAMPLES / name).read_text())
        moment = datetime.now(UTC) - timedelta(days=1)
        raw["snapshot_at"] = moment.strftime("%Y-%m-%dT%H:%M:%SZ")
        path = tmp_path / f"fresh-{name}"
        path.write_text(json.dumps(raw))
        return path

    return make
