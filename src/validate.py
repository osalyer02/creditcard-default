from __future__ import annotations
import argparse
import json
from pathlib import Path
import pandas as pd
from pandera.errors import SchemaErrors
from .schema import feature_schema, target_schema, ALL_FEATURES, TARGET

def load_and_standardize(csv_path: Path):
    """Load CSV and standardize column names."""
    df = pd.read_csv(csv_path)
    # Rename the target if it uses the original UCI name
    if "default.payment.next.month" in df.columns:
        df = df.rename(columns={"default.payment.next.month": TARGET})
    expected = [c for c in ALL_FEATURES if c in df.columns]
    cols = expected + ([TARGET] if TARGET in df.columns else [])
    missing = sorted(list(set(ALL_FEATURES) - set(df.columns)))
    return df[cols], missing

def run_validation(df: pd.DataFrame):
    """Validate features and target separately."""
    f_errors = None
    try:
        _ = feature_schema.validate(df[[c for c in df.columns if c != TARGET]], lazy=True)
    except SchemaErrors as err:
        f_errors = err

    t_errors = None
    if TARGET in df.columns:
        try:
            _ = target_schema.validate(df[[TARGET]], lazy=True)
        except SchemaErrors as err:
            t_errors = err

    return f_errors, t_errors

def summarize_errors(err: SchemaErrors | None):
    """Summarize Pandera SchemaErrors into JSON-friendly dict."""
    if err is None:
        return {"error_count": 0, "sample_failure_cases": [], "failure_case_columns": []}
    fc = err.failure_cases
    sample = fc.head(50).to_dict(orient="records")
    return {
        "error_count": int(len(fc)),
        "sample_failure_cases": sample,
        "failure_case_columns": sorted(set(fc["column"].dropna().astype(str))) if "column" in fc else [],
    }

def main():
    ap = argparse.ArgumentParser(description="Validate UCI Credit Default raw dataset.")
    ap.add_argument("--in", dest="input_csv", required=True, help="Path to UCI_Credit_Card.csv")
    ap.add_argument("--out", dest="out_json", required=True, help="Where to write validation_report.json")
    args = ap.parse_args()

    csv_path = Path(args.input_csv)
    out_path = Path(args.out_json)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if not csv_path.exists():
        raise SystemExit(f"Input CSV not found: {csv_path}")

    df, missing = load_and_standardize(csv_path)
    f_errors, t_errors = run_validation(df)

    report = {
        "input_csv": str(csv_path),
        "row_count": int(df.shape[0]),
        "columns_present": sorted(df.columns.tolist()),
        "missing_expected_columns": missing,
        "features_validation": summarize_errors(f_errors),
        "target_validation": summarize_errors(t_errors),
        "passed": (len(missing) == 0)
                   and (f_errors is None)
                   and ((TARGET not in df.columns) or (t_errors is None)),
    }

    out_path.write_text(json.dumps(report, indent=2))
    if not report["passed"]:
        # print concise summary for CLI feedback
        print(json.dumps({
            "missing_expected_columns": missing,
            "features_validation": report["features_validation"],
            "target_validation": report["target_validation"]
        }, indent=2))
        raise SystemExit(1)

    print(f"Validation passed. Report written to {out_path}")

if __name__ == "__main__":
    main()
