import math

from analysis import rms_priority_order
from model import Task


def hyperperiod(tasks: list[Task]) -> int:
    # Гиперпериод - наименьшее общее кратное периодов всех задач.
    return math.lcm(*(task.t for task in tasks))



def simulate_rms(tasks: list[Task], interval: int) -> dict[str, list[bool]]:
    # Пошаговая симуляция RMS с вытеснением (шаг 1 мс).
    # Возвращает для каждой задачи список из interval значений:
    # True — в этот миллисекундный такт задача выполнялась.
    order = rms_priority_order(tasks)
    timeline = {task.name: [False] * interval for task in order}
    ready = []  # активные работы: [приоритет, задача, момент появления, осталось]

    for now in range(interval):
        # Новые работы появляются в моменты, кратные периоду
        for priority, task in enumerate(order):
            if now % task.t == 0:
                ready.append([priority, task, now, task.c])
        if not ready:
            continue
        # Выполняется работа с наивысшим приоритетом (при равенстве — более ранняя)
        job = min(ready, key=lambda j: (j[0], j[2]))
        timeline[job[1].name][now] = True
        job[3] -= 1
        if job[3] == 0:
            ready.remove(job)
    return timeline



def gantt(tasks: list[Task], interval: int) -> str:
    # Текстовая временная диаграмма RMS на интервале [0, interval].
    # Строки идут в порядке приоритета (сверху — самый высокий),
    # █ — задача выполняется, · — не выполняется.

    timeline = simulate_rms(tasks, interval)
    width = max(len(name) for name in timeline)

    # Шкала времени: отметка каждые 5 мс
    scale = [" "] * (interval + 2)  # запас под многозначную последнюю отметку
    for tick in range(0, interval + 1, 5):
        for k, ch in enumerate(str(tick)):
            if tick + k < len(scale):
                scale[tick + k] = ch
    lines = [" " * width + " |" + "".join(scale)]

    for name, ticks in timeline.items():
        row = "".join("█" if busy else "·" for busy in ticks)
        lines.append(f"{name.ljust(width)} |{row}")
    return "\n".join(lines)