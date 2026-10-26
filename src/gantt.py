import math

from analysis import rms_priority_order
from model import Task


def hyperperiod(tasks: list[Task]) -> int:
    # Гиперпериод - наименьшее общее кратное периодов всех задач.
    return math.lcm(*(task.t for task in tasks))