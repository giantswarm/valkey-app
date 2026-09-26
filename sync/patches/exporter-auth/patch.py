"""Hand the metrics exporter the default user's password when auth is on.

Without it redis_exporter connects unauthenticated and scrapes nothing but
`redis_up 0`. Upstream ships the same env entry from 0.9 on, where this edit
is a no-op.
"""

import sys

sys.path.insert(0, "sync")
from patchlib import edit  # noqa: E402

edit(
    "templates/deploy_valkey.yaml",
    """            - name: REDIS_ALIAS
              value: {{ include "valkey.fullname" . }}
""",
    """            - name: REDIS_ALIAS
              value: {{ include "valkey.fullname" . }}
            {{- if .Values.auth.enabled }}
            - name: REDIS_PASSWORD
              valueFrom:
                secretKeyRef:
                  {{- if .Values.auth.usersExistingSecret }}
                  {{- $defaultUser := index .Values.auth.aclUsers "default" | default dict }}
                  {{- $passwordKey := $defaultUser.passwordKey | default "default" }}
                  name: {{ tpl .Values.auth.usersExistingSecret . }}
                  key: {{ $passwordKey }}
                  {{- else }}
                  name: {{ include "valkey.fullname" . }}-auth
                  key: default-password
                  {{- end }}
            {{- end }}
""",
    "REDIS_PASSWORD for the exporter",
)
