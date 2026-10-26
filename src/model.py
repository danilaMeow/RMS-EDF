from dataclasses import dataclass


@dataclass(frozen=True)
class Task:
    #Периодическая задача τ = (C, T, D). Время - в миллисекундах.

    name: str  # имя задачи
    c: int     # время выполнения
    t: int     # период
    d: int     # относительный дедлайн
    
    def __post_init__(self) -> None:
        # Проверка, что параметры имеют смысл
        if self.c <= 0 or self.t <= 0 or self.d <= 0:
            raise ValueError(f"Задача {self.name}: C, T и D должны быть положительными")
        if self.c > self.d:
            raise ValueError(f"Задача {self.name}: C больше дедлайна D, задача заведомо не успеет")