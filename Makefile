clean:
	find . -name '__pycache__' -exec rm -fr {} +
	rm -rf ./.cache .mypy_cache ./schema/.mypy_cache .coverage

test:
	pytest

PROJECT = backend
COVFILE ?= .coverage

coverage-application:
	@echo "Executing..."
	pytest --cov=$(PROJECT)/application \
	$(PROJECT)/tests/ --cov-report term-missing -x -s -W \
	ignore::DeprecationWarning -o cache_dir=/tmp/application/cache

clean_pycache:
	@echo "Cleaning pycache..."
	@find . -name "*.pyc" -exec rm -rf {} \;
	@find . -name "__pycache__" -exec rm -rf {} \;
	@echo "Done."