#!/usr/bin/env bash

# Fail when helm/valkey/charts/valkey is not the upstream chart vendir.yml pins
# plus the Giant Swarm delta in sync/patches/, or when the credential checksum
# does not hash what the chart's Secret carries. `make verify-sync` runs it; it
# needs vendir, helm, python3 and the network (the upstream chart repository).

set -o errexit
set -o nounset
set -o pipefail

# The patches import sync/patchlib.py; keep the tree free of its bytecode.
export PYTHONDONTWRITEBYTECODE=1

cd "$(git rev-parse --show-toplevel)"

readonly chart=helm/valkey
readonly subchart=${chart}/charts/valkey

scratch=$(mktemp -d)
trap 'rm -rf "${scratch}"' EXIT

fail=0
note() {
	echo "$1" >&2
	fail=1
}

# The tree must be what `make update-chart` produces from the pinned version.
cp vendir.yml vendir.lock.yml "${scratch}/"
vendir sync --locked --chdir "${scratch}" >/dev/null
for patch in sync/patches/*/patch.py ; do
	VALKEY_CHART_DIR="${scratch}/${subchart}" python3 "${patch}"
done
if ! diff -r "${scratch}/${subchart}" "${subchart}" ; then
	note "${subchart} is not the pinned upstream chart plus sync/patches; run 'make update-chart' (the delta goes into sync/patches, never into the vendored tree)"
fi

field() { # field <key> <Chart.yaml>: a top-level scalar, quotes stripped
	sed -n "s/^$1:[[:space:]]*[\"']\{0,1\}\([^\"'[:space:]]*\).*/\1/p" "$2"
}
sub_version=$(field version "${subchart}/Chart.yaml")
sub_app_version=$(field appVersion "${subchart}/Chart.yaml")
[ "$(field appVersion "${chart}/Chart.yaml")" == "${sub_app_version}" ] \
	|| note "${chart}/Chart.yaml appVersion is not the vendored chart's ${sub_app_version}; run 'make update-chart'"
grep -A2 -- '- name: valkey' "${chart}/Chart.yaml" | grep -q "version: ${sub_version}$" \
	|| note "${chart}/Chart.yaml does not depend on the vendored valkey ${sub_version}; run 'make update-chart'"

# checksum/auth-secret hashes valkey.authSecretData, which mirrors the data
# block of upstream's secret.yaml; an upstream change to that block would
# silently stop the pod from rolling on the new keys.
creds=(--set auth.enabled=true
	--set auth.aclUsers.default.permissions='~* &* +@all' --set auth.aclUsers.default.password=one
	--set auth.aclUsers.reader.permissions='~* +@read' --set auth.aclUsers.reader.password=two
	--set auth.aclConfig='user extra on >three ~* +@read')
data=$(helm template verify "${subchart}" "${creds[@]}" --show-only templates/secret.yaml \
	| sed -n '/^data:/,$p' | sed '1d; s/^  //')
want=$(printf '%s' "${data}" | sha256sum | cut -d' ' -f1)
got=$(helm template verify "${subchart}" "${creds[@]}" --show-only templates/deploy_valkey.yaml \
	| sed -n 's/^ *checksum\/auth-secret: "\{0,1\}\([0-9a-f]*\)"\{0,1\}$/\1/p')
[ "${got}" == "${want}" ] \
	|| note "checksum/auth-secret (${got:-none}) is not the SHA-256 of the rendered Secret's data (${want}); align valkey.authSecretData in sync/patches/auth-checksum with templates/secret.yaml"

exit "${fail}"
