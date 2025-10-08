import pytest
from airport import *

class TestAircraft:
    def test_aircraft_creation(self):
        aircraft = Aircraft("Boeing 737", 180, "RA-73651")
        assert aircraft.model == "Boeing 737"
        assert aircraft.capacity == 180
        assert aircraft.registration == "RA-73651"
    def test_aircraft_str(self):
        aircraft = Aircraft("Airbus A320", 150, "RA-32042")
        assert "Airbus A320" in str(aircraft)
        assert "RA-32042" in str(aircraft)

class TestPassenger:
    def test_passenger_creation(self):
        passenger = Passenger("AB123456", "Иван", "Петров", "Иванович", "1985-05-15")
        assert passenger.passport == "AB123456"
        assert passenger.name == "Иван"
        assert passenger.full_name == "Петров Иван Иванович"
    def test_passenger_booking(self):
        passenger = Passenger("AB123456", "Иван", "Петров", "Иванович", "1985-05-15")
        passenger.book_flight("SU-1001")
        assert "SU-1001" in passenger.get_booked_flights()


class TestFlight:
    def setup_method(self):
        self.aircraft = Aircraft("Boeing 737", 2, "RA-73651")
        self.passenger1 = Passenger("AB123456", "Иван", "Петров", "Иванович", "1985-05-15")
        self.passenger2 = Passenger("CD789012", "Мария", "Иванова", "Денисовна", "1990-08-22")
    def test_flight_creation(self):
        flight = Flight("SU-1001", "Москва", "СПб", "2025-01-20 08:00", self.aircraft, 90)
        assert flight.flight_number == "SU-1001"
        assert flight.departure == "Москва"
        assert not flight.is_cancelled
    def test_add_passenger(self):
        flight = Flight("SU-1001", "Москва", "СПб", "2025-01-20 08:00", self.aircraft, 90)
        assert flight.add_passenger(self.passenger1) == True
        assert flight.passenger_count == 1
        assert flight.add_passenger(self.passenger1) == False
        assert flight.passenger_count == 1
    def test_flight_occupancy(self):
        flight = Flight("SU-1001", "Москва", "СПб", "2025-01-20 08:00", self.aircraft, 90)
        flight.add_passenger(self.passenger1)
        flight.add_passenger(self.passenger2)
        assert flight.occupancy_rate == 100.0
        assert flight.available_seats == 0

    def test_flight_cancellation(self):
        flight = Flight("SU-1001", "Москва", "СПб", "2024-01-20 08:00", self.aircraft, 90)
        flight.add_passenger(self.passenger1)
        flight.cancel_flight()
        assert flight.is_cancelled == True
        assert flight.passenger_count == 0