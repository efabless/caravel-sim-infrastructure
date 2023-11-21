PACKAGE_NAME = caravel_cocotb

.PHONY: clean test lint dist upload release

clean:
	rm -rf dist build *.egg-info
	rm -rf caravel mgmt_core pdk_root user_project_root

test:
	pip install .
	python3 caravel_cocotb/CI/main.py

lint:
	flake8

dist: clean
	python3 setup.py sdist bdist_wheel

upload: dist
	twine upload dist/*

release: lint test dist upload
	
