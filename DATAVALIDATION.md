## Validate Data (with conda)
1) Place the raw CSV at `data/raw/UCI_Credit_Card.csv`
2) Create+activate conda environment called **credit-default** with Python 3.11 via:
```bash
conda create -y -n credit-default python=3.11
```
and:
```bash
conda activate credit-default
```
3) Run:
```bash
pip install -U pip && pip install -r requirements.txt
```
4) 