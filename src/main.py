import argparse
import sys
from pathlib import Path

from analysis import (
    edf_schedulable,
    liu_layland_bound,
    response_times,
    rms_schedulable,
    utilization,
)
from gantt import gantt, hyperperiod
from loader import load_tasks

# Файл по умолчанию лежит в data/ рядом с папкой src/
DEFAULT_FILE = Path(__file__).resolve().parent.parent / "data" / "zadachi.json"


def print_table(tasks) -> None:
    # Печатает таблицу «Задача | C | T | D | R | Уложилась».
    rows = [("Задача", "C", "T", "D", "R", "Уложилась")]
    for task, r, ok in response_times(tasks):
        rows.append((task.name, str(task.c), str(task.t), str(task.d), str(r), "Да" if ok else "Нет"))
    widths = [max(len(row[i]) for row in rows) for i in range(6)]
    for k, row in enumerate(rows):
        print(" | ".join(cell.ljust(widths[i]) for i, cell in enumerate(row)))
        if k == 0:
            print("-+-".join("-" * w for w in widths))