import csv
import random
from pathlib import Path


def read_csv(file_path: str | Path) -> list[dict]:
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)


def select_random_row(file_path: str | Path) -> dict:
    rows = read_csv(file_path)
    return random.choice(rows)


def select_random_rows(file_path: str | Path, count: int) -> list[dict]:
    rows = read_csv(file_path)
    return random.sample(rows, min(count, len(rows)))
