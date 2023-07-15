.PHONY: install format lint test

SHELL = bash
CPU_CORES = $$(( $(shell nproc) > 4 ? 4 : $(shell nproc) ))

all: install format lint test

INSTALLED := .installed
install: $(INSTALLED)
$(INSTALLED):
	poetry install
	touch $(INSTALLED)

format: install
	poetry run black .
	poetry run isort .

lint: install
	poetry run black . --diff --check
	poetry run isort . --check
	poetry run pylint --jobs=$(CPU_CORES) find_closed_references tests
	poetry run mypy find_closed_references tests || true

test: install
	poetry run pytest -n $(CPU_CORES) --color=yes -v tests

release: lint test
	./scripts/release.sh
