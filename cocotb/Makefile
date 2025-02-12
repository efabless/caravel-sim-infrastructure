PACKAGE_NAME = caravel_cocotb

PYTHON3 ?= python3

all: dist

.PHONY: upload
upload: dist
	./venv/bin/python3 -m pip install twine
	./venv/bin/twine upload dist/*

.PHONY: dist
dist: venv/manifest.txt
	./venv/bin/poetry build
	
.PHONY: lint
lint: venv/manifest.txt
	./venv/bin/flake8 .
	
test: venv/manifest.txt
	./venv/bin/python3 -m pip install .
	./venv/bin/python3 caravel_cocotb/CI/main.py

venv: venv/manifest.txt
venv/manifest.txt: ./pyproject.toml ./poetry.lock
	rm -rf venv
	python3 -m venv ./venv
	PYTHONPATH= ./venv/bin/python3 -m pip install --upgrade pip
	PYTHONPATH= ./venv/bin/python3 -m pip install --upgrade wheel poetry poetry-plugin-export
	PYTHONPATH= ./venv/bin/poetry export --with dev --without-hashes --format=requirements.txt --output=requirements_tmp.txt
	PYTHONPATH= ./venv/bin/python3 -m pip install --upgrade -r requirements_tmp.txt
	PYTHONPATH= ./venv/bin/python3 -m pip freeze > $@
	@echo ">> Venv prepared."

.PHONY: clean
clean:
	rm -rf _nl2bench_antlr4*/
	rm -rf build/
	rm -rf dist/
	rm -rf htmlcov/
	rm -rf *.egg-info/
	rm -rf .antlr/
	rm -f .coverage
