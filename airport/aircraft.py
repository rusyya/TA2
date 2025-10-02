from abc import ABC, abstractmethod

__all__ = ['Aircraft']


class Aircraft(ABC):
    def __init__(self, model: str, capacity: int, registration: str):
        self._model = model
        self._capacity = capacity
        self._registration = registration
        self._is_available = True

    @property
    def model(self):
        return self._model
    @property
    def capacity(self):
        return self._capacity
    @property
    def registration(self):
        return self._registration
    @property
    def is_available(self):
        return self._is_available

    @is_available.setter
    def is_available(self, value: bool):
        self._is_available = value

    @abstractmethod
    def get_aircraft_info(self):
        pass

    def __str__(self):
        return f"{self._model} ({self._registration}) - Capacity: {self._capacity}"
    def __repr__(self):
        return f"Aircraft(model='{self._model}', capacity={self._capacity}, registration='{self._registration}')"


class Aircraft(Aircraft):
    def get_aircraft_info(self):
        return (f"Самолёт: {self._model}\n"
                f"Регистрация: {self._registration}\n"
                f"Вместимость: {self._capacity}")
    def __eq__(self, other):
        if isinstance(other, Aircraft):
            return self._registration == other._registration
        return False
    def __gt__(self, other):
        if isinstance(other, Aircraft):
            return self._capacity > other._capacity
        return False