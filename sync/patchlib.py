"""Anchored, idempotent text edits for the patches under sync/patches/.

Every edit names the upstream text it expects. A file that already carries the
Giant Swarm text is left alone, so a patch can run twice and a change upstream
adopts verbatim drops out on its own. A file with neither fails the sync with
the file and the edit named: upstream reworked it, and the patch has to be
re-derived against the new text.
"""

import os
import sys

CHART = os.environ.get("VALKEY_CHART_DIR", "helm/valkey/charts/valkey")


def path(rel):
    return os.path.join(CHART, rel)


def exists(rel):
    return os.path.exists(path(rel))


def edit(rel, old, new, name):
    """Replace the one occurrence of old with new in the chart file rel."""
    p = path(rel)
    with open(p, encoding="utf-8") as f:
        content = f.read()
    if new in content:
        return
    count = content.count(old)
    if count != 1:
        sys.exit(
            f"{p}: {name}: expected the upstream text once, found it {count} times. "
            "Upstream reworked the file: re-derive the patch against the new text."
        )
    with open(p, "w", encoding="utf-8") as f:
        f.write(content.replace(old, new))


def edit_all(rel, old, new, name):
    """Replace every occurrence of old with new in the chart file rel."""
    p = path(rel)
    with open(p, encoding="utf-8") as f:
        content = f.read()
    if old not in content:
        if new in content:
            return
        sys.exit(
            f"{p}: {name}: the upstream text is gone. "
            "Upstream reworked the file: re-derive the patch against the new text."
        )
    with open(p, "w", encoding="utf-8") as f:
        f.write(content.replace(old, new))


def append(rel, block):
    """Append block to the chart file rel unless it is already there."""
    p = path(rel)
    with open(p, encoding="utf-8") as f:
        content = f.read()
    if block in content:
        return
    if not content.endswith("\n"):
        content += "\n"
    with open(p, "w", encoding="utf-8") as f:
        f.write(content + block)
