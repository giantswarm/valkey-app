"""Roll the Valkey pod when its users' credentials change.

The init container reads the passwords once, at pod start, and the metrics
exporter reads the default user's password at start, so a changed password
has to restart the pod. Beside upstream's checksum/initconfig and
checksum/config the pod template gets:

- checksum/auth-secret: the SHA-256 of the <fullname>-auth Secret's data, while
  the chart renders that Secret (inline passwords or aclConfig);
- checksum/users-secret: auth.usersExistingSecretChecksum verbatim, the mark
  whoever rotates auth.usersExistingSecret (which the chart cannot read)
  changes with it.

The auth Secret volume is mounted only while the chart renders the Secret:
upstream mounts it for inline passwords even with auth off, where the Secret
does not exist and the pod never starts.
"""

import re
import sys

sys.path.insert(0, "sync")
from patchlib import append, edit, edit_all, exists, path  # noqa: E402

append(
    "templates/_helpers.tpl",
    """
{{/*
Whether the chart renders the <fullname>-auth Secret: auth on with an inline
password or an inline ACL configuration.
*/}}
{{- define "valkey.renderAuthSecret" -}}
{{- if and .Values.auth.enabled (or (include "valkey.hasInlinePasswords" . | eq "true") .Values.auth.aclConfig) -}}
true
{{- else -}}
false
{{- end -}}
{{- end -}}

{{/*
Data of the <fullname>-auth Secret (templates/secret.yaml), one "key: base64"
line per entry: the inline passwords and the inline ACL configuration. Its
SHA-256 is the pod template's checksum/auth-secret annotation. It mirrors the
Secret template's data block; sync/verify.sh renders both and fails when they
disagree.
*/}}
{{- define "valkey.authSecretData" -}}
{{- $lines := list -}}
{{- range $username, $user := .Values.auth.aclUsers -}}
{{- if $user.password -}}
{{- $lines = append $lines (printf "%s-password: %s" $username ($user.password | b64enc)) -}}
{{- end -}}
{{- end -}}
{{- if .Values.auth.aclConfig -}}
{{- $lines = append $lines (printf "aclConfig: %s" (.Values.auth.aclConfig | b64enc)) -}}
{{- end -}}
{{- join "\\n" $lines -}}
{{- end -}}

{{/*
The pod template's credential checksums, one "annotation: value" line each:
checksum/auth-secret while the chart renders the auth Secret, and
checksum/users-secret while auth.usersExistingSecret and
auth.usersExistingSecretChecksum are set. Empty while auth is off.
*/}}
{{- define "valkey.authChecksums" -}}
{{- $lines := list -}}
{{- if .Values.auth.enabled -}}
{{- if include "valkey.renderAuthSecret" . | eq "true" -}}
{{- $lines = append $lines (printf "checksum/auth-secret: %q" (include "valkey.authSecretData" . | sha256sum)) -}}
{{- end -}}
{{- if and .Values.auth.usersExistingSecret .Values.auth.usersExistingSecretChecksum -}}
{{- $lines = append $lines (printf "checksum/users-secret: %q" .Values.auth.usersExistingSecretChecksum) -}}
{{- end -}}
{{- end -}}
{{- join "\\n" $lines -}}
{{- end -}}
""",
)

# Every workload template upstream ships (the Deployment, and from 0.9 on the
# StatefulSet) gets the checksums after its checksum/config block and mounts
# the auth Secret only while it is rendered.
annotations = """        {{- with include "valkey.authChecksums" . }}
        {{- . | nindent 8 }}
        {{- end }}
"""
config_checksum = re.compile(r"( +checksum/config: [^\n]*\n +\{\{- end \}\}\n)")
for workload in ("templates/deploy_valkey.yaml", "templates/statefulset.yaml"):
    if workload != "templates/deploy_valkey.yaml" and not exists(workload):
        continue
    with open(path(workload), encoding="utf-8") as f:
        content = f.read()
    anchors = config_checksum.findall(content)
    if len(anchors) != 1:
        sys.exit(
            f"{path(workload)}: credential checksums: expected one checksum/config "
            f"block, found {len(anchors)}. Re-derive the patch against the new text."
        )
    edit(workload, anchors[0], anchors[0] + annotations, "credential checksums")
    edit_all(
        workload,
        """{{- if or (include "valkey.hasInlinePasswords" . | eq "true") .Values.auth.aclConfig }}""",
        """{{- if include "valkey.renderAuthSecret" . | eq "true" }}""",
        "auth Secret volume only while rendered",
    )

edit(
    "values.yaml",
    """  usersExistingSecret: ""
""",
    """  usersExistingSecret: ""

  # A mark of the existing secret's revision, rendered verbatim as the pod
  # template's checksum/users-secret annotation. The chart cannot read the
  # secret, and the init container reads it once: change this value in the
  # same change that rotates a password (a hash over the new data, a counter,
  # a date) so the pod restarts onto it. While empty, a rotation of the
  # existing secret alone leaves the running Valkey on the old passwords.
  usersExistingSecretChecksum: ""
""",
    "auth.usersExistingSecretChecksum value",
)

edit(
    "values.schema.json",
    """                "usersExistingSecret": {
                    "type": "string"
                }
""",
    """                "usersExistingSecret": {
                    "type": "string"
                },
                "usersExistingSecretChecksum": {
                    "type": "string"
                }
""",
    "auth.usersExistingSecretChecksum schema",
)
