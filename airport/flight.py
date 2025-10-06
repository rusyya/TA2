from abc import ABC, abstractmethod
from datetime import datetime, timedelta

__all__ = ['Flight']

from airport import Aircraft
from airport import Passenger


class Flight(ABC):
    def __init__(self, flight_number: str, departure: str, destination: str, departure_time: str, aircraft: Aircraft, duration_min: int):
        self._flight_number = flight_number
        self._departure = departure
        self._destination = destination
        self._departure_time = datetime.strptime(departure_time, "%Y-%m-%d %H:%M")
        self._aircraft = aircraft
        self._duration_min = duration_min
        self._passengers = []
        self._is_cancelled = False


    @property
    def flight_number(self):
        return self._flight_number
    @property
    def departure(self):
        return self._departure
    @property
    def destination(self):
        return self._destination
    @property
    def departure_time(self):
        return self._departure_time
    @property
    def aircraft(self):
        return self._aircraft
    @property
    def duration_min(self):
        return self._duration_min
    @property
    def arrival_time(self):
        return self._departure_time + timedelta(minutes=self._duration_min)
    @property
    def is_cancelled(self):
        return self._is_cancelled
    @is_cancelled.setter
    def is_cancelled(self, value: bool):
        self._is_cancelled = value
    @property
    def passenger_count(self):
        return len(self._passengers)
    @property
    def available_seats(self):
        return self._aircraft.capacity - self.passenger_count
    @property
    def occupancy_rate(self):
        return self.passenger_count / self._aircraft.capacity * 100


    def add_passenger(self, passenger: 'Passenger') -> bool:
        if self.passenger_count >= self._aircraft.capacity:
            return False
        if passenger not in self._passengers:
            self._passengers.append(passenger)
            passenger.book_flight(self._flight_number)
            return True
        return False

    def remove_passenger(self, passenger:'Passenger'):
        if passenger in self._passengers:
            self._passengers.remove(passenger)

    def get_passengers(self):
        return self._passengers.copy()

    def cancel_flight(self):
        self._is_cancelled = True
        self._passengers.clear()

    def get_flight_info(self):
        status = "Отменён" if self._is_cancelled else "По расписанию"
        return (
            f"Рейс № {self._flight_number}"
            f"Из: {self.departure}, время: {self._departure_time.strftime('%Y-%m-%d %H:%M')}"
            f"До: {self.destination}, время: {self.arrival_time.strftime('%Y-%m-%d %H:%M')}"
            f"Время в пути (мин): {self._duration_min}"
            f"Самолёт: {self._aircraft.model}"
            f"Пассажиры: {self.passenger_count}/{self._aircraft.capacity}, {self.occupancy_rate}%"
            f"Статус: {status}")

    def __str__(self):
        status = "Отменён" if self._is_cancelled else "По расписанию"
        return f"{self._flight_number}: {self._departure} → {self._destination} ({status})"
    def __repr__(self):
        return f"Flight(number='{self._flight_number}', departure='{self._departure}', destination='{self._destination}')"
    def __contains__(self, passenger):
        return passenger in self._passengers
    def __len__(self):
        return len(self._passengers)