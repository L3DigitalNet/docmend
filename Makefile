GO_FILES := $(shell git ls-files --cached --others --exclude-standard -- '*.go')
GOLANGCI_LINT := .tools/bin/golangci-lint
GOLANGCI_LINT_VERSION := v2.12.2
GOLANGCI_LINT_PACKAGE := github.com/golangci/golangci-lint/v2/cmd/golangci-lint

.PHONY: go-tools go-format go-format-check go-config go-vet go-lint go-test go-build go-audit go-mod-check go-check

go-tools:
	mkdir -p .tools/bin
	GOBIN="$(CURDIR)/.tools/bin" go install $(GOLANGCI_LINT_PACKAGE)@$(GOLANGCI_LINT_VERSION)

go-format:
	@if [ -n "$(GO_FILES)" ]; then gofmt -w $(GO_FILES); fi

go-format-check:
	@if [ -n "$(GO_FILES)" ]; then \
		files="$$(gofmt -l $(GO_FILES))"; \
		if [ -n "$$files" ]; then printf '%s\n' "$$files"; exit 1; fi; \
	fi

go-vet:
	@packages="$$(go list ./...)" || exit $$?; \
	if [ -n "$$packages" ]; then go vet $$packages; else echo "No Go packages yet; vet skipped."; fi

go-config: $(GOLANGCI_LINT)
	$(GOLANGCI_LINT) config verify

go-lint:
	@packages="$$(go list ./...)" || exit $$?; \
	if [ -n "$$packages" ]; then $(MAKE) $(GOLANGCI_LINT); $(GOLANGCI_LINT) run $$packages; else echo "No Go packages yet; lint skipped."; fi

$(GOLANGCI_LINT):
	$(MAKE) go-tools

go-test:
	@packages="$$(go list ./...)" || exit $$?; \
	if [ -n "$$packages" ]; then go test -race -cover $$packages; else echo "No Go packages yet; tests skipped."; fi

go-build:
	@packages="$$(go list ./...)" || exit $$?; \
	if [ -n "$$packages" ]; then go build $$packages; else echo "No Go packages yet; build skipped."; fi

go-audit:
	@packages="$$(go list ./...)" || exit $$?; \
	if [ -n "$$packages" ]; then go tool govulncheck $$packages; else echo "No Go packages yet; vulnerability scan skipped."; fi

go-mod-check:
	go mod tidy -diff
	go mod verify

go-check: go-format-check go-mod-check go-config go-vet go-lint go-test go-build go-audit
