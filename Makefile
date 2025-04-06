#!/usr/bin/make -f

MAKEFLAGS+=--warn-undefined-variables
SHELL:=/bin/bash
.SHELLFLAGS:=-eu -o pipefail -c
.DEFAULT_GOAL:=help
.SILENT:

# all targets are phony
.PHONY: $(shell egrep -o ^[a-zA-Z_-]+: $(MAKEFILE_LIST) | sed 's/://')

fix: install format test

install: ## install
	echo 'Starting $@'
	uv sync
	echo 'Finished $@'

format: ## format
	echo 'Starting $@'
	uv run isort src tests
	uv run black src tests
	echo 'Finished $@'

test: ## test
	echo 'Starting $@'
	uv run python -m unittest discover -v
	echo 'Finished $@'

help: ## Print this help
	echo 'Usage: make [target]'
	echo ''
	echo 'Targets:'
	awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
