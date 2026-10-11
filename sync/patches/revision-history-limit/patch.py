"""Cap the Deployment's retained ReplicaSets with a revisionHistoryLimit value.

Upstream sets none, so Kubernetes keeps ten old ReplicaSets, and their old pod
templates keep failing policies the current one passes. The value defaults to 3.
"""

import sys

sys.path.insert(0, "sync")
from patchlib import edit  # noqa: E402

edit(
    "templates/deploy_valkey.yaml",
    """  replicas: 1
  strategy:
""",
    """  replicas: 1
  revisionHistoryLimit: {{ .Values.revisionHistoryLimit }}
  strategy:
""",
    "Deployment revisionHistoryLimit",
)

edit(
    "values.yaml",
    """# Annotations for the Deployment/StatefulSet resource
workloadAnnotations: {}
""",
    """# Annotations for the Deployment/StatefulSet resource
workloadAnnotations: {}

# Old ReplicaSets the Deployment keeps (Kubernetes' own default is 10)
revisionHistoryLimit: 3
""",
    "revisionHistoryLimit value",
)

edit(
    "values.schema.json",
    """        "workloadAnnotations": {
            "type": "object"
        }
""",
    """        "revisionHistoryLimit": {
            "type": "integer",
            "minimum": 0
        },
        "workloadAnnotations": {
            "type": "object"
        }
""",
    "revisionHistoryLimit schema",
)
