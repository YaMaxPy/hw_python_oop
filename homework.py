from __future__ import annotations
from dataclasses import dataclass

import sys


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:0.3f} ч.; '
                f'Дистанция: {self.distance:0.3f} км; '
                f'Ср. скорость: {self.speed:0.3f} км/ч; '
                f'Потрачено ккал: {self.calories:0.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    H_IN_MIN: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 len_step: float = LEN_STEP,
                 m_in_km: int = M_IN_KM,
                 h_in_min: int = H_IN_MIN,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        self.LEN_STEP = len_step
        self.M_IN_KM = m_in_km
        self.H_IN_MIN = h_in_min

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            f'''Переопределите {sys._getframe().f_code.co_name}
             в классе {self.__class__.__name__}''')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    K_1_RUN: int = 18
    K_2_RUN: int = 20

    def __init__(self,
                 action,
                 duration,
                 weight,
                 k_1_run: int = K_1_RUN,
                 k_2_run: int = K_2_RUN,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.K_1_RUN = k_1_run
        self.K_2_RUN = k_2_run

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.K_1_RUN * self.get_mean_speed() - self.K_2_RUN)
                * self.weight / self.M_IN_KM * self.duration * self.H_IN_MIN)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    K_1_WLK: float = 0.035
    K_2_WLK: float = 0.029

    def __init__(self,
                 action,
                 duration,
                 weight,
                 height: float,
                 k_1_wlk: float = K_1_WLK,
                 k_2_wlk: float = K_2_WLK,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height
        self.K_1_WLK = k_1_wlk
        self.K_2_WLK = k_2_wlk

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        mean_speed = super().get_mean_speed()
        return ((self.K_1_WLK * self.weight + (mean_speed ** 2 // self.height)
                * self.K_2_WLK * self.weight) * self.duration * self.H_IN_MIN)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    K_1_SWM: float = 1.1

    def __init__(self,
                 action,
                 duration,
                 weight,
                 length_pool: int,
                 count_pool: int,
                 len_step: float = LEN_STEP,
                 k_1_swm: float = K_1_SWM,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool
        self.LEN_STEP = len_step
        self.K_1_SWM = k_1_swm

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (self.get_mean_speed() + self.K_1_SWM) * 2 * self.weight


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_codes: dict[str, type[Training]] = {'SWM': Swimming,
                                                 'RUN': Running,
                                                 'WLK': SportsWalking}
    if workout_type in training_codes:
        return training_codes[workout_type](*data)
    else:
        raise KeyError(f'{workout_type} - неизвестный тип тренировки')


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
