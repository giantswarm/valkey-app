"""Render the pod template's annotations key whether or not podAnnotations is set.

Upstream 0.8.x opens `annotations:` inside `with .Values.podAnnotations`, so
without pod annotations the checksum lines below it land under `labels:`: the
checksums then never roll the pod, and a label value longer than 63 characters
is rejected. Upstream fixed it the same way in 0.9, where this edit is a no-op.
"""

import sys

sys.path.insert(0, "sync")
from patchlib import edit  # noqa: E402

edit(
    "templates/deploy_valkey.yaml",
    """      {{- with .Values.podAnnotations }}
      annotations:
        {{- toYaml . | nindent 8 }}
      {{- end }}
""",
    """      annotations:
        {{- with .Values.podAnnotations }}
        {{- toYaml . | nindent 8 }}
        {{- end }}
""",
    "annotations key outside podAnnotations",
)
