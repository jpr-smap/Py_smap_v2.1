from __future__ import annotations

import csv
from typing import Dict


def summarize_parity_map(csv_path: str) -> Dict[str, int]:
    """Summarize a parity map CSV produced by :mod:`indexer`."""

    counts: Dict[str, int] = {"matched": 0, "matlab_only": 0, "python_only": 0}
    with open(csv_path, newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            has_m = bool(row["matlab"].strip())
            has_p = bool(row["python"].strip())
            if has_m and has_p:
                counts["matched"] += 1
            elif has_m:
                counts["matlab_only"] += 1
            elif has_p:
                counts["python_only"] += 1
    return counts


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Summarize a parity map CSV")
    parser.add_argument("csv_path")
    args = parser.parse_args()
    counts = summarize_parity_map(args.csv_path)
    for key, val in counts.items():
        print(f"{key}: {val}")


if __name__ == "__main__":  # pragma: no cover - CLI entry
    main()
