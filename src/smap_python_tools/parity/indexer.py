from __future__ import annotations

import csv
import os
from typing import Iterable, List, Tuple


def _matlab_files(root: str) -> Iterable[str]:
    for dirpath, _, filenames in os.walk(root):
        for name in filenames:
            if name.endswith(".m"):
                yield os.path.join(dirpath, name)


def _python_files(root: str) -> Iterable[str]:
    for dirpath, _, filenames in os.walk(root):
        for name in filenames:
            if name.endswith(".py"):
                yield os.path.join(dirpath, name)


def build_parity_map(matlab_root: str, python_root: str, csv_path: str) -> List[Tuple[str, str]]:
    """Create a parity map CSV linking MATLAB and Python files."""

    rows: List[Tuple[str, str]] = []
    python_set = {
        os.path.relpath(p, python_root).replace(os.sep, "/"): p for p in _python_files(python_root)
    }

    for m in _matlab_files(matlab_root):
        rel = os.path.relpath(m, matlab_root).replace(os.sep, "/")
        candidate = rel[:-2] + ".py" if rel.endswith(".m") else rel
        py = python_set.pop(candidate, "")
        rows.append((m, py))

    for remaining in python_set.values():
        rows.append(("", remaining))

    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    with open(csv_path, "w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["matlab", "python"])
        writer.writerows(rows)

    return rows


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Generate MATLAB/Python parity map")
    parser.add_argument("matlab_root")
    parser.add_argument("python_root")
    parser.add_argument("output", nargs="?", default="reports/parity_map.csv")
    args = parser.parse_args()
    build_parity_map(args.matlab_root, args.python_root, args.output)


if __name__ == "__main__":  # pragma: no cover - CLI entry
    main()
