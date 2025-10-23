.PHONY: install validate clean env

ENV_NAME := credit-default
PYTHON := python

# Create a conda environment and get requirements
env:
	conda create -y -n $(ENV_NAME) $(PYTHON)=3.11
	conda activate $(ENV_NAME) && pip install -U pip && pip install -r requirements.txt

install: env

# Validate the raw dataset (expects data/raw/UCI_Credit_Card.csv)
validate:
	conda run -n $(ENV_NAME) $(PYTHON) -m src.validate --in data/raw/UCI_Credit_Card.csv --out reports/validation_report.json

clean:
	conda env remove -n $(ENV_NAME) -y
	rm -rf __pycache__ .pytest_cache .mypy_cache
