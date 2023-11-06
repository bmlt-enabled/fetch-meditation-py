help:  ## Print the help documentation
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY:
composer: $(VENDOR_AUTOLOAD) ## Runs composer install

.PHONY: lint
lint:  ## Py Lint
	pycodestyle --exclude='venv/*' --ignore=E501 .

.PHONY: fmt
fmt:  ## Py Fmt
	autopep8 --exclude='*/venv/*' --in-place --recursive .
