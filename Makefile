# Dev workflow wrappers, so the rarely-used commands don't need remembering.
# Run `make` (or `make help`) to see this list.
#
# One-time machine setup: `make setup` (installs Homebrew Ruby + project gems).
# Day to day: `make serve`, then edit; push to main to deploy.

SHELL := /bin/zsh
RUBY_BIN := /opt/homebrew/opt/ruby/bin
export PATH := $(RUBY_BIN):$(PATH)

.DEFAULT_GOAL := help

help: ## Show this help
	@grep -hE '^[a-z-]+:.*##' $(MAKEFILE_LIST) | awk -F ':.*## ' '{printf "  make %-12s %s\n", $$1, $$2}'

serve: ## Local preview at http://localhost:4000 (rebuilds on save; Ctrl-C to stop)
	bundle exec jekyll serve --watch

build: ## Build the site into _site/ (what CI does on every push)
	bundle exec jekyll build

setup: ## One-time per machine: install Homebrew Ruby and project gems
	brew install ruby
	bundle config set --local path vendor/bundle
	bundle install

update-gems: ## Refresh gems after editing Gemfile or updating Ruby
	bundle install

scrape: ## List upcoming GSO concerts (then: make scrape ARGS="--import 1,3")
	uv run scripts/scrape_gso_concerts.py $(ARGS)

.PHONY: help serve build setup update-gems scrape
