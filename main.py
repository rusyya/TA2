from airport import *
from datetime import datetime
import sqlite3
import os


class AirportSystem:

    def __init__(self, db_name='airport.db'):
        self.db_name = db_name
        self.aircrafts = []
        self.passengers = []
        self.flights = []
        self.init_database()
        self.load_from_database()

    def init_database(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS aircrafts (
                registration TEXT PRIMARY KEY,
                model TEXT NOT NULL,
                capacity INTEGER NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS passengers (
                passport TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                surname TEXT NOT NULL,
                patronymic TEXT NOT NULL,
                date_of_birth TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS flights (
                flight_number TEXT PRIMARY KEY,
                departure TEXT NOT NULL,
                destination TEXT NOT NULL,
                departure_time TEXT NOT NULL,
                aircraft_registration TEXT NOT NULL,
                duration_minutes INTEGER NOT NULL,
                is_cancelled INTEGER DEFAULT 0,
                FOREIGN KEY (aircraft_registration) REFERENCES aircrafts (registration)
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                flight_number TEXT NOT NULL,
                passenger_passport TEXT NOT NULL,
                booking_time TEXT NOT NULL,
                FOREIGN KEY (flight_number) REFERENCES flights (flight_number),
                FOREIGN KEY (passenger_passport) REFERENCES passengers (passport)
            )
        ''')
        conn.commit()
        conn.close()

    def load_from_database(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM aircrafts')
        for row in cursor.fetchall():
            reg, model, capacity = row
            aircraft = Aircraft(model, capacity, reg)
            self.aircrafts.append(aircraft)
        cursor.execute('SELECT * FROM passengers')
        for row in cursor.fetchall():
            passport, name, surname, patronymic, dob = row
            passenger = Passenger(passport, name, surname, patronymic, dob)
            self.passengers.append(passenger)
        cursor.execute('SELECT * FROM flights')
        for row in cursor.fetchall():
            number, dep, dest, dep_time, aircraft_reg, duration, cancelled = row
            aircraft = next((x for x in self.aircrafts if x.registration == aircraft_reg), None)
            if aircraft:
                flight = Flight(number, dep, dest, dep_time, aircraft, duration)
                flight.is_cancelled = bool(cancelled)
                self.flights.append(flight)
        cursor.execute('SELECT * FROM bookings')
        for row in cursor.fetchall():
            _, flight_num, passport, _ = row
            flight = next((f for f in self.flights if f.flight_number == flight_num), None)
            passenger = next((p for p in self.passengers if p.passport == passport), None)
            if flight and passenger:
                flight.add_passenger(passenger)
        conn.close()

    def save_aircraft(self, aircraft):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO aircrafts 
            (registration, model, capacity)
            VALUES (?, ?, ?)
        ''', (aircraft.registration, aircraft.model, aircraft.capacity))
        conn.commit()
        conn.close()
        self.aircrafts.append(aircraft)

    def del_aircraft(self):
        pass

    def save_passenger(self, passenger):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO passengers 
            (passport, name, surname, patronymic, date_of_birth)
            VALUES (?, ?, ?, ?, ?)
        ''', (passenger.passport, passenger.name, passenger.surname, passenger.patronymic, passenger.date_of_birth.strftime('%Y-%m-%d')))
        conn.commit()
        conn.close()
        self.passengers.append(passenger)

    def save_flight(self, flight):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO flights 
            (flight_number, departure, destination, departure_time, aircraft_registration, 
             duration_minutes, is_cancelled)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (flight.flight_number, flight.departure, flight.destination,
              flight.departure_time.strftime('%Y-%m-%d %H:%M'), flight.aircraft.registration,
              flight.duration_min, int(flight.is_cancelled)))
        conn.commit()
        conn.close()
        self.flights.append(flight)

    def save_booking(self, flight, passenger):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO bookings (flight_number, passenger_passport, booking_time)
            VALUES (?, ?, ?)
        ''', (flight.flight_number, passenger.passport, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        conn.commit()
        conn.close()


    def display_statistics(self):
        print("АЭРОПОРТ - СТАТИСТИКА")
        print(f"Всего самолетов: {len(self.aircrafts)}")
        print(f"Всего пассажиров: {len(self.passengers)}")
        print(f"Всего рейсов: {len(self.flights)}")
        active_flights = [f for f in self.flights if not f.is_cancelled]
        cancelled_flights = [f for f in self.flights if f.is_cancelled]
        print(f"Активных рейсов: {len(active_flights)}")
        print(f"Отмененных рейсов: {len(cancelled_flights)}")
        if active_flights:
            avg_occupancy = sum(f.occupancy_rate for f in active_flights) / len(active_flights)
            print(f"Средняя заполненность: {avg_occupancy:.1f}%")
        print("\nСамолеты:")
        for aircraft in self.aircrafts:
            status = "Доступен" if aircraft.is_available else "Не доступен"
            print(f"  - {aircraft}")
    def run(self):
        while True:
            print("СИСТЕМА УПРАВЛЕНИЯ АЭРОПОРТОМ")
            print("1. РАБОТА С БД")
            print("2. РАБОТА С РЕЙСАМИ")
            print("3. СТАТИСТИКА")
            print("4. ВЫХОД")
            choice = input("ВВОД: ").strip()
            if choice == '1':
                while True:
                    print("РАБОТА С БД")
                    print("1. ДОБАВИТЬ САМОЛЁТ")
                    print("2. УДАЛИТЬ САМОЛЁТ")
                    print("3. ДОБАВИТЬ ПАССАЖИРА")
                    print("4. УДАЛИТЬ ПАССАЖИРА")
                    print("5. ВЫХОД")
                    choice = input("ВВОД: ").strip()
                    if choice == '1':
                        print("ДОБАВЛЕНИЕ САМОЛЁТА")
                        name = input("Имя: ")
                        capacity = int(input("Вместимость: "))
                        id_air = input("Номер: ")
                        self.save_aircraft(Aircraft(name, capacity, id_air))
                    elif choice == '2':
                        print("УДАЛЕНИЕ САМОЛЁТА")
                    elif choice == '3':
                        print("ДОБАВЛЕНИЕ ПАССАЖИРА")
                        surname = input("Фамилия: ")
                        name = input("Имя: ")
                        patronymic = input("Отчество: ")
                        passport = input("Паспорт: ")
                        dob = input("Дата рождения: ")
                        self.save_passenger(Passenger(passport, name, surname, patronymic, dob))
                    elif choice == '4':
                        print("УДАЛЕНИЕ ПАССАЖИРА")
                    elif choice == '5':
                        break
                    else:
                        print("Неверный выбор. Попробуйте снова.")
            elif choice == '2':
                while True:
                    print("РАБОТА С РЕЙСАМИ")
                    print("1. ДОБАВИТЬ РЕЙС")
                    print("2. ОТМЕНИТЬ РЕЙС")
                    print("3. ДОБАВИТЬ ПАССАЖИРА НА РЕЙС")
                    print("4. СНЯТЬ ПАССАЖИРА С РЕЙСА")
                    print("5. ПОКАЗАТЬ РЕЙСЫ")
                    print("6. ВЫХОД")
                    choice = input("ВВОД: ").strip()
                    if choice == '1':
                        print("ДОБАВЛЕНИЕ РЕЙСА")
                        self.add_new_flight()
                    elif choice == '2':
                        print("УДАЛЕНИЕ РЕЙСА")
                        self.cancel_flight()
                    elif choice == '3':
                        print("ДОБАВЛЕНИЕ ПАССАЖИРА НА РЕЙС")
                        self.add_passenger_to_flight()
                    elif choice == '4':
                        print("УДАЛЕНИЕ ПАССАЖИРА С РЕЙСА")
                    elif choice == '5':
                        print("ПОКАЗАТЬ РЕЙСЫ")
                        self.show_flight_info()
                    elif choice == '6':
                        break
                    else:
                        print("Неверный выбор. Попробуйте снова.")
            elif choice == '3':
                self.display_statistics()
            elif choice == '4':
                break
            else:
                print("Неверный выбор. Попробуйте снова.")

    def add_passenger_to_flight(self):
        print("ДОБАВЛЕНИЕ ПАССАЖИРА НА РЕЙС")
        active_flights = [f for f in self.flights if not f.is_cancelled]
        if not active_flights:
            print("Нет активных рейсов.")
            return
        print("Активные рейсы:")
        for i, flight in enumerate(active_flights, 1):
            print(
                f"{i}. {flight.flight_number}: {flight.departure} → {flight.destination} (свободно мест: {flight.available_seats})")
        try:
            flight_choice = int(input("Выберите рейс: ")) - 1
            selected_flight = active_flights[flight_choice]
        except (ValueError, IndexError):
            print("Неверный выбор рейса.")
            return
        print("\nВведите данные пассажира:")
        passport = input("Номер паспорта: ")
        surname = input("Фамилия: ")
        name = input("Имя: ")
        patronymic = input("Отчество: ")
        dob = input("Дата рождения (ГГГГ-ММ-ДД): ")
        try:
            new_passenger = Passenger(passport, name, surname, patronymic, dob)
            self.save_passenger(new_passenger)
            if selected_flight.add_passenger(new_passenger):
                self.save_booking(selected_flight, new_passenger)
                print(f"Пассажир {new_passenger.full_name} успешно добавлен на рейс {selected_flight.flight_number}")
                print(f"Заполненность рейса: {selected_flight.occupancy_rate}%")
                print(f"Свободно мест: {selected_flight.available_seats}")
            else:
                print("Не удалось добавить пассажира. Рейс заполнен!")
                if selected_flight.passenger_count >= selected_flight.aircraft.capacity:
                    print("Рейс отменен из-за недостатка мест!")
                    selected_flight.cancel_flight()
                    conn = sqlite3.connect(self.db_name)
                    cursor = conn.cursor()
                    cursor.execute('UPDATE flights SET is_cancelled = 1 WHERE flight_number = ?',(selected_flight.flight_number,))
                    conn.commit()
                    conn.close()
        except ValueError as e:
            print(f"Ошибка в данных: {e}")

    def add_new_flight(self):
        available_aircrafts = [x for x in self.aircrafts if x.is_available]
        if not available_aircrafts:
            print("Нет доступных самолётов")
        try:
            flight_number = input("Номер рейса: ").strip()
            if not flight_number:
                print("Номер не может быть пустым")
                return
            if next((x for x in self.flights if x.flight_number == flight_number), None):
                print("Рейс уже существует")
            departure = input("Город вылета: ").strip()
            if not departure:
                print("Город вылета не может быть пустым")
                return
            destination = input("Город назначения: ")
            if not destination:
                print("Город назначения не может быть пустым")
                return
            departure_time = input("Вылет: ГГГГ-ММ-ДД ЧЧ:ММ ").strip()
            try:
                datetime.strptime(departure_time, "%Y-%m-%d %H:%M")
            except ValueError:
                print("Неверный формат")
                return
            try:
                duration_min = int(input("Длительность (мин): "))
                if duration_min <= 0:
                    print("Введите положительное число: ")
                    return
            except ValueError:
                print("Введите число")
                return
            print("Доступные самолёты:")
            for i, aircraft in enumerate(available_aircrafts, 1):
                print(f"{i}. {aircraft.model} ({aircraft.registration}) - {aircraft.capacity} мест")
            try:
                aircraft_choice = int(input("Выберите самолёт: ")) - 1
                if aircraft_choice < 0 or aircraft_choice >= len(available_aircrafts):
                    print("Неверный выбор")
                    return
                selected_aircraft = available_aircrafts[aircraft_choice]
            except (ValueError, IndexError):
                print("Неверный выбор")
                return
            self.save_flight(Flight(flight_number, departure, destination, departure_time, selected_aircraft, duration_min))
        except Exception as e:
            print(f"Ошибка при создании рейса: {e}")

    def cancel_flight(self):
        print("ОТМЕНА РЕЙСА")
        active_flights = [f for f in self.flights if not f.is_cancelled]
        if not active_flights:
            print("Нет активных рейсов для отмены.")
            return
        print("Активные рейсы:")
        for i, flight in enumerate(active_flights, 1):
            print(f"{i}. {flight.flight_number}: {flight.departure} → {flight.destination}")
        try:
            flight_choice = int(input("Выберите рейс для отмены: ")) - 1
            selected_flight = active_flights[flight_choice]
            selected_flight.cancel_flight()
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('UPDATE flights SET is_cancelled = 1 WHERE flight_number = ?',(selected_flight.flight_number,))
            conn.commit()
            conn.close()
            print(f"Рейс {selected_flight.flight_number} отменен.")
        except (ValueError, IndexError):
            print("Неверный выбор рейса.")

    def show_flight_info(self):
        print("ИНФОРМАЦИЯ О РЕЙСАХ")
        if not self.flights:
            print("Нет рейсов.")
            return
        print("Все рейсы:")
        for i, flight in enumerate(self.flights, 1):
            print(f"{i}. {flight.flight_number}: {flight.departure} → {flight.destination}")
        try:
            flight_choice = int(input("Выберите рейс: ")) - 1
            selected_flight = self.flights[flight_choice]
            print(f"\n{selected_flight.get_flight_info()}")
            if selected_flight.passenger_count > 0:
                print("\nПассажиры:")
                for passenger in selected_flight.get_passengers():
                    print(f"  - {passenger.full_name} (Паспорт: {passenger.passport})")
            else:
                print("\nНа рейсе нет пассажиров")
        except (ValueError, IndexError):
            print("Неверный выбор рейса.")


if __name__ == "__main__":
    system = AirportSystem()
    system.run()