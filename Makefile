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
	autopep8 --exclude='*/venv/*' --in-place --recursive ./fetch_meditation/

.PHONY: test
test:  ## Py Test
	poetry run pytest
