##@ Helm

HELM_UNITTEST_VERSION := 1.0.3
CHART := helm/valkey
SUBCHART := $(CHART)/charts/valkey

.PHONY: helm-lint
helm-lint: ## Lint the wrapper chart and the vendored subchart.
	helm lint $(CHART)
	helm lint $(SUBCHART)

.PHONY: helm-test
helm-test: helm-lint helm-unittest ## Run every chart check (what the chart-test CI job runs).

.PHONY: helm-unittest
helm-unittest: helm-plugin-unittest ## Run the helm-unittest suites in $(SUBCHART)/tests/.
	helm unittest $(SUBCHART)

.PHONY: helm-plugin-unittest
helm-plugin-unittest:
	@helm plugin list | grep -q '^unittest' || helm plugin install https://github.com/helm-unittest/helm-unittest --version $(HELM_UNITTEST_VERSION)
