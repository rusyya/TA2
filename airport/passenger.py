from datetime import datetime

__all__ = ['Passenger']


class Passenger:
    def __init__(self, passport: str, name: str, surname: str, patronymic: str, date_of_birth: str):
        self._passport = passport
        self._name = name
        self._surname = surname
        self._patronymic = patronymic
        self._date_of_birth = datetime.strptime(date_of_birth, "%Y-%m-%d").date()
        self._booked_flights = []

    @property
    def passport(self):
        return self._passport
    @property
    def name(self):
        return self._name
    @property
    def surname(self):
        return self._surname
    @property
    def patronymic(self):
        return self._patronymic
    @property
    def full_name(self):
        return f"{self._surname} {self._name} {self._patronymic}"
    @property
    def age(self):
        today = datetime.now().date()
        return today.year - self._date_of_birth.year - ((today.month, today.day) < (self._date_of_birth.month, self._date_of_birth.day))

    def book_flight(self, flight_number: str):
        self._booked_flights.append(flight_number)
    def get_booked_flights(self):
        return self._booked_flights.copy()

    def __str__(self):
        return f"Пассажир: {self.full_name} (Паспорт: {self._passport})"
    def __repr__(self):
        return f"Passenger(passport='{self._passport}', name='{self._name}', surname='{self._surname}', patronymic='{self._patronymic}')"
    def __eq__(self, other):
        if isinstance(other, Passenger):
            return self._passport == other._passport
        return False