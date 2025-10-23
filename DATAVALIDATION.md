## How to run (with conda)
1) Place the raw CSV at `data/raw/UCI_Credit_Card.csv`
2) Create and install the conda environment:
```bash
make install
```
This creates a new environment called **credit-default** with Python 3.11 and all necessary packages.

3) Run validation:
```bash
make validate
```
A report will be written to `reports/validation_report.json`

4) To remove the conda environment after report generation:
```bash
make clean
```