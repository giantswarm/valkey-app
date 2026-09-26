##@ Chart

# Consumed by the generated App targets (Makefile.gen.app.mk), so
# `make update-chart` needs no APPLICATION= on the command line.
APPLICATION := valkey

HELM_UNITTEST_VERSION := 1.0.3
CHART := helm/$(APPLICATION)
SUBCHART := $(CHART)/charts/valkey

# The generated update-chart runs `vendir sync` and then update-deps, which
# re-applies the Giant Swarm delta to the freshly vendored chart first.
update-deps: sync-patches

.PHONY: sync-patches
sync-patches: ## Re-apply the Giant Swarm delta (sync/patches) to the vendored chart.
	./sync/patch.sh

.PHONY: verify-sync
verify-sync: ## Fail when the vendored chart is not upstream plus sync/patches.
	./sync/verify.sh

.PHONY: helm-lint
helm-lint: ## Lint the wrapper chart and the vendored subchart.
	helm lint $(CHART)
	helm lint $(SUBCHART)

.PHONY: helm-test
helm-test: helm-lint helm-unittest verify-sync ## Run every chart check (what the chart-test CI job runs).

.PHONY: helm-unittest
helm-unittest: helm-plugin-unittest ## Run the helm-unittest suites in tests/chart/ against the vendored chart.
	helm unittest --file '../../../../tests/chart/*_test.yaml' $(SUBCHART)

.PHONY: helm-plugin-unittest
helm-plugin-unittest:
	@helm plugin list | grep -q '^unittest' || helm plugin install https://github.com/helm-unittest/helm-unittest --version $(HELM_UNITTEST_VERSION)
