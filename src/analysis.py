from model import Task


def utilization(tasks: list[Task]) -> float:
    # Коэффициент загрузки U = Σ C/T.
    return sum(task.c / task.t for task in tasks)