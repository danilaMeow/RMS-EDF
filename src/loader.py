import csv
import json
from pathlib import Path

from model import Task


def _row_to_task(row: dict) -> Task:
    # Превращает словарь с ключами name, C, T, D в задачу.
    return Task(str(row["name"]), int(row["C"]), int(row["T"]), int(row["D"]))


def load_json(path: Path) -> list[Task]:
    # Читает задачи из JSON: {"tasks": [{"name": ..., "C": ..., "T": ..., "D": ...}]}.
    data = json.loads(path.read_text(encoding="utf-8"))
    return [_row_to_task(row) for row in data["tasks"]]


def load_csv(path: Path) -> list[Task]:
    # Читает задачи из CSV с заголовком name,C,T,D.
    with path.open(encoding="utf-8", newline="") as f:
        return [_row_to_task(row) for row in csv.DictReader(f)]