from datetime import datetime

__all__ = ['Passenger']


class Passenger:
    def __init__(self, passport: str, name: str, surname: str, date_of_birth: str):
        self._passport = passport
        self._name = name
        self._surname = surname
        self._date_of_birth = datetime.strptime(date_of_birth, "%Y-%m-%d").date()
        self._booked_flights = []