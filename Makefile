.PHONY: setup lint test format app

setup:
	pip install -U pip
	pip install -r requirements.txt
	pre-commit install

lint:
	black --check .
	isort --check-only .
	flake8 .
	mypy src

format:
	black .
	isort .

test:
	pytest

app:
	streamlit run app/streamlit/Home.py
