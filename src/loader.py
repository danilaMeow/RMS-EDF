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
    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        text = raw.decode("cp1251")  # файл сохранён в Windows-1251
    return [_row_to_task(row) for row in csv.DictReader(text.splitlines())]

def load_tasks(path: str | Path) -> list[Task]:
    # Выбирает формат по расширению файла (.json или .csv).
    path = Path(path)
    readers = {".json": load_json, ".csv": load_csv}
    reader = readers.get(path.suffix.lower())
    if reader is None:
        raise ValueError(f"Неподдерживаемый формат файла: {path.suffix} (нужен .json или .csv)")
    tasks = reader(path)
    if not tasks:
        raise ValueError("В файле нет ни одной задачи")
    return tasks