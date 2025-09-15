.PHONY: venv run test

venv:
	python -m venv .venv

run:
	source .venv/bin/activate && python src/pipeline.py --date 2025-08-31

test:
	pytest -q
