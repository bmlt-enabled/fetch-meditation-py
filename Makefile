help:  ## Print the help documentation
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: build
build:  ## Py build package
	poetry build

.PHONY: lint
lint:  ## Py Lint
	pycodestyle --exclude='venv/*' --ignore=E501 ./fetch_meditation/

.PHONY: fmt
fmt:  ## Py Fmt
	poetry run black ./fetch_meditation/

.PHONY: test
test:  ## Py Test
	poetry run pytest

.PHONY: docs
docs:  ## Generate documentation
	cd docs && poetry run make html

.PHONY: docs-serve
docs-serve:  ## Serve documentation locally
	@echo "Serving documentation at http://127.0.0.1:8000/_build/html/"
	@cd docs && poetry run python -m http.server
