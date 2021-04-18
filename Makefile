.PHONY: help
help: ## Show this text.
	# https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: all
all: lambda.zip template.yaml ## Build a package.

lambda.zip: awslambda/macro.py awslambda/resource.py
	cd awslambda && zip ../lambda.zip macro.py resource.py

.PHONY: test
test: ## Run tests.
	python -m pytest tests/ -v

template.yaml: template.template.yaml VERSION
	perl -pe 's!%%VERSION%%!'"$(shell cat VERSION)"'!g' $< > $@

.PHONY: clean
clean: ## Remove generated files.
	@rm -f packaged.yaml
	@rm -f lambda.zip
