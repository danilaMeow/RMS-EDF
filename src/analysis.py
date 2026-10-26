import math

from model import Task


def utilization(tasks: list[Task]) -> float:
    # Коэффициент загрузки U = Σ C/T.
    return sum(task.c / task.t for task in tasks)

def liu_layland_bound(n: int) -> float:
    # Граница Liu & Layland для RMS: n·(2^(1/n) − 1).
    if n < 1:
        raise ValueError("Число задач должно быть не меньше 1")
    return n * (2 ** (1 / n) - 1)

def rms_schedulable(tasks: list[Task]) -> bool:
    
    # Утилизационный тест Liu & Layland для RMS.
    # Условие достаточное: если U выше границы, это ещё не значит,
    # что набор непланируем — нужен анализ времени отклика.
    
    return utilization(tasks) <= liu_layland_bound(len(tasks))

def edf_schedulable(tasks: list[Task]) -> bool:

    # Условие планируемости EDF для неявных дедлайнов (D = T): U ≤ 1.
    # Если у какой-то задачи D < T, условие U ≤ 1 остаётся только необходимым.

    return utilization(tasks) <= 1

def rms_priority_order(tasks: list[Task]) -> list[Task]:
    # Приоритеты RMS: меньший период - выше приоритет (первый в списке — самый высокий).
    return sorted(tasks, key=lambda task: task.t)



def response_time(task: Task, higher: list[Task]) -> int:
    # Время отклика по рекуррентной формуле: R = C + Σ ceil(R / Tj) · Cj.
    # higher — задачи с более высоким приоритетом. Итерация начинается с R = C
    # и останавливается, когда значение перестало меняться. Если R превысило
    # дедлайн, возвращается это значение (задача не укладывается).
    r = task.c
    while True:
        r_next = task.c + sum(math.ceil(r / h.t) * h.c for h in higher)
        if r_next == r:
            return r
        if r_next > task.d:
            return r_next
        r = r_next