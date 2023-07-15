.PHONY: install format lint test

SHELL = bash
CPU_CORES = $$(( $(shell nproc) > 4 ? 4 : $(shell nproc) ))
