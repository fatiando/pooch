# Build, package, test, and clean
PROJECT=pooch
TESTS=tests src/$(PROJECT)
PYTEST_ARGS=--cov-config=.coveragerc --cov-report=term-missing --cov=$(PROJECT) --doctest-modules -v --pyargs
LINT_FILES=$(PROJECT)
CHECK_STYLE=src/$(PROJECT) doc

.PHONY: help build install test format check check-format check-style lint clean

help:
	@echo "Commands:"
	@echo ""
	@echo "  install   install in editable mode"
	@echo "  test      run the test suite (including doctests) and report coverage"
	@echo "  format    automatically format the code"
	@echo "  check     run code style and quality checks"
	@echo "  lint      run pylint for a deeper (and slower) quality check"
	@echo "  build     build source and wheel distributions"
	@echo "  clean     clean up build and generated files"
	@echo ""

build:
	python -m build .

install:
	python -m pip install --no-deps -e .

test:
	pytest $(PYTEST_ARGS) $(TESTS)

format:
	black $(CHECK_STYLE)
	burocrata --extension=py $(CHECK_STYLE)

check: check-format check-style

check-format:
	black --check $(CHECK_STYLE)
	burocrata --check --extension=py $(CHECK_STYLE)

check-style:
	flake8 $(CHECK_STYLE)

lint:
	pylint --jobs=0 $(LINT_FILES)

clean:
	find . -name "*.pyc" -exec rm -v {} \;
	find . -name "*.orig" -exec rm -v {} \;
	find . -name ".coverage.*" -exec rm -v {} \;
	rm -rvf build dist MANIFEST *.egg-info __pycache__ .coverage .cache .pytest_cache src/$(PROJECT)/_version.py
	rm -rvf dask-worker-space
