#!/usr/bin/env bash

# Re-apply the Giant Swarm delta to the vendored upstream chart
# (helm/valkey/charts/valkey) and carry its appVersion onto the wrapper chart.
# `make update-chart` runs it after `vendir sync`; it is idempotent, so running
# it on an already patched tree changes nothing. VALKEY_CHART_DIR points it at
# another copy of the vendored chart (sync/verify.sh uses that).
#
# Each sync/patches/<name>/patch.py is a set of anchored edits that fails
# loudly when upstream reworks the text it expects (sync/patchlib.py).

set -o errexit
set -o nounset
set -o pipefail

# The patches import sync/patchlib.py; keep the tree free of its bytecode.
export PYTHONDONTWRITEBYTECODE=1

cd "$(git rev-parse --show-toplevel)"

for patch in sync/patches/*/patch.py ; do
	python3 "${patch}"
done

# The wrapper packages the upstream application: its appVersion is the one the
# vendored chart declares, so the catalog shows the Valkey version it deploys.
python3 - <<'PY'
import os, re

chart = os.environ.get("VALKEY_CHART_DIR", "helm/valkey/charts/valkey")
with open(os.path.join(chart, "Chart.yaml"), encoding="utf-8") as f:
    app_version = re.search(r"^appVersion:\s*[\"']?([^\"'\s]+)", f.read(), re.M).group(1)

wrapper = "helm/valkey/Chart.yaml"
with open(wrapper, encoding="utf-8") as f:
    content = f.read()
content = re.sub(r"^appVersion:.*$", f"appVersion: {app_version}", content, count=1, flags=re.M)
with open(wrapper, "w", encoding="utf-8") as f:
    f.write(content)
PY
