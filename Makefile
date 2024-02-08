run_tests:
	pytest

run_cov:
	pytest --cov

flake:
	.venv/bin/python -m flake8 --append-config .flake8 .
black:
	.venv/bin/python -m black .

linter:
	make black
	make flake