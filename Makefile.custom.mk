##@ Chart

# Consumed by the generated App targets (Makefile.gen.app.mk), so
# `make update-chart` needs no APPLICATION= on the command line.
APPLICATION := valkey

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

# Prerequisite-only, no recipe: make merges it into the generated helm-test
# rule, which keeps its recipe and gains these checks. That recipe finds no
# suite under helm/ and says so, as the suites live in tests/: tests/chart/
# asserts on the vendored subchart, which `vendir sync` replaces whole.
.PHONY: helm-test
helm-test: helm-lint helm-unittest verify-sync

.PHONY: helm-unittest
helm-unittest: install-helm-unittest ## Run the helm-unittest suites: tests/chart/ against the vendored chart, tests/wrapper/ against the wrapper with its subchart (the wrapper's defaults rendered through the vendored workloads).
	helm unittest --file '../../../../tests/chart/*_test.yaml' $(SUBCHART)
	helm unittest --file '../../tests/wrapper/*_test.yaml' $(CHART)
