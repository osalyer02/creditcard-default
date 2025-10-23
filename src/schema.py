from __future__ import annotations
import pandera as pa
from pandera import Column, DataFrameSchema, Check

# === Column groups ===
CATEGORICAL = ["SEX", "EDUCATION", "MARRIAGE"]
PAY_STATUS = [f"PAY_{i}" for i in range(1, 7)]
BILL_AMTS = [f"BILL_AMT{i}" for i in range(1, 7)]
PAY_AMTS = [f"PAY_AMT{i}" for i in range(1, 7)]
NUMERIC = ["LIMIT_BAL", "AGE"] + PAY_STATUS + BILL_AMTS + PAY_AMTS
ALL_FEATURES = CATEGORICAL + NUMERIC
TARGET = "default_payment_next_month"

# === Feature schema ===
feature_schema = DataFrameSchema(
    {
        # basic demographics
        "LIMIT_BAL": Column(pa.Float, Check.ge(0), nullable=False, coerce=True),
        "SEX": Column(pa.Int, Check.isin([1, 2]), nullable=False, coerce=True),
        "EDUCATION": Column(pa.Int, Check.isin([0, 1, 2, 3, 4, 5, 6]), nullable=False, coerce=True),
        "MARRIAGE": Column(pa.Int, Check.isin([0, 1, 2, 3]), nullable=False, coerce=True),
        "AGE": Column(pa.Int, Check.between(18, 125), nullable=False, coerce=True),

        # payment status codes
        **{col: Column(pa.Int, Check.between(-2, 9), nullable=False, coerce=True)
           for col in PAY_STATUS},

        **{col: Column(pa.Float, nullable=False, coerce=True) for col in BILL_AMTS},
        **{col: Column(pa.Float, Check.ge(0), nullable=False, coerce=True) for col in PAY_AMTS},
    },
    strict="filter",   # ignore unexpected columns
)

# === Target schema ===
target_schema = DataFrameSchema(
    {TARGET: Column(pa.Int, Check.isin([0, 1]), nullable=False, coerce=True)},
    strict=True,
)
