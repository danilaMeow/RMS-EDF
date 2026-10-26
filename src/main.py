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



def print_tests(tasks) -> None:
    # Печатает загрузку U и выводы по тесту Liu & Layland и по EDF.
    u = utilization(tasks)
    n = len(tasks)
    bound = liu_layland_bound(n)
    terms = " + ".join(f"{t.c}/{t.t}" for t in tasks)
    print(f"Загрузка: U = {terms} = {u:.3f}")

    if rms_schedulable(tasks):
        verdict = "набор планируем по RMS"
    else:
        verdict = "тест не пройден (условие достаточное — смотрите время отклика)"
    sign = "≤" if u <= bound else ">"
    print(f"RMS (Liu & Layland): n = {n}, граница = {bound:.3f}; U = {u:.3f} {sign} {bound:.3f} — {verdict}")

    edf_text = "набор планируем по EDF" if edf_schedulable(tasks) else "набор не планируем по EDF"
    sign = "≤" if u <= 1 else ">"
    print(f"EDF: U = {u:.3f} {sign} 1 — {edf_text}")
    if any(t.d != t.t for t in tasks):
        print("Внимание: у части задач D ≠ T, для EDF условие U ≤ 1 в этом случае только необходимое.")



def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Анализ планируемости RMS и EDF")
    parser.add_argument("file", nargs="?", default=DEFAULT_FILE, help="файл задач (.json или .csv)")
    args = parser.parse_args()

    tasks = load_tasks(args.file)
    print_table(tasks)
    print()
    print_tests(tasks)

    all_ok = all(ok for _, _, ok in response_times(tasks))
    print("По времени отклика:", "все задачи укладываются в дедлайны" if all_ok else "есть задачи, не укладывающиеся в дедлайн")

    period = hyperperiod(tasks)
    print(f"\nДиаграмма выполнения по RMS на интервале [0, {period}] (гиперпериод):")
    print(gantt(tasks, period))


if __name__ == "__main__":
    main()