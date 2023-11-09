from datetime import datetime

class Person:
    def __init__(self, name, contact_info):
        self.name = name
        self.contact_info = contact_info

    def __str__(self):
        return f"Person: {self.name}"

class Driver(Person):
    def __init__(self, name, contact_info, vehicle_capacity):
        super().__init__(name, contact_info)
        self.vehicle_capacity = vehicle_capacity
        self.available_seats = vehicle_capacity

    def __str__(self):
        return f"Driver: {self.name}, Vehicle Capacity: {self.vehicle_capacity}, Available Seats: {self.available_seats}"

class Passenger(Person):
    def __init__(self, name, contact_info):
        super().__init__(name, contact_info)
        self.preferred_travel_time = None

    def __str__(self):
        return f"Passenger: {self.name}"

class Trip:
    def __init__(self, driver, passengers, start_time, destination, recurring=False, recurrence_days=None):
        self.driver = driver
        self.passengers = passengers
        self.start_time = start_time
        self.destination = destination
        self.recurring = recurring
        self.recurrence_days = recurrence_days
        self.active = True

    def cancel_trip(self):
        self.active = False

    def reschedule_trip(self, new_time):
        self.start_time = new_time

    def __str__(self):
        passenger_names = ', '.join([passenger.name for passenger in self.passengers])
        recurrence_info = f", Recurs on: {', '.join(self.recurrence_days)}" if self.recurring else ""
        return (f"{'Active' if self.active else 'Cancelled'} Trip: {self.destination}, "
                f"Driver: {self.driver.name}, Passengers: {passenger_names}, "
                f"Start Time: {self.start_time.strftime('%Y-%m-%d %H:%M')}{recurrence_info}")

class CarpoolGroup:
    def __init__(self):
        self.drivers = []
        self.passengers = []
        self.trips = []
        self.driver_ratings = {}  

    def add_driver(self, driver):
        self.drivers.append(driver)
        self.driver_ratings[driver] = []  

    def add_passenger(self, passenger):
        self.passengers.append(passenger)

    def create_trip(self, driver, passengers, start_time, destination, recurring=False, recurrence_days=None):
        if driver in self.drivers and all(passenger in self.passengers for passenger in passengers):
            new_trip = Trip(driver, passengers, start_time, destination, recurring, recurrence_days)
            self.trips.append(new_trip)
            return new_trip
        else:
            return None

    def match_passengers_to_driver(self, driver, preferred_times):
        #Matching passengers to a driver based on preferred travel times.
        matched_passengers = []
        for passenger in self.passengers:
            if passenger.preferred_travel_time in preferred_times:
                matched_passengers.append(passenger)
        return matched_passengers

    def rate_driver(self, driver, rating):
        # Rating a driver on a scale of 1-5.
        if driver in self.driver_ratings:
            self.driver_ratings[driver].append(rating)
            return True
        else:
            return False

    def get_driver_rating(self, driver):
        ## Calculating the average rating of a driver.
        if driver in self.driver_ratings and self.driver_ratings[driver]:
            return sum(self.driver_ratings[driver]) / len(self.driver_ratings[driver])
        else:
            return "No ratings yet"

    def __str__(self):
        return (f"CarpoolGroup with {len(self.drivers)} drivers, "
                f"{len(self.passengers)} passengers, and {len(self.trips)} trips planned.")


driver_example = Driver("Baje Masak", "555-0101", 4)
passenger_example = Passenger("Peter Paul", "555-0102")

carpool_group = CarpoolGroup()
carpool_group.add_driver(driver_example)
carpool_group.add_passenger(passenger_example)

passenger_example.preferred_travel_time = datetime(2023, 11, 10, 8, 0)

# Matching passengers to a driver for a trip
matched_passengers = carpool_group.match_passengers_to_driver(driver_example, [passenger_example.preferred_travel_time])

# Rate a driver
carpool_group.rate_driver(driver_example, 5)
carpool_group.rate_driver(driver_example, 4)

# Get driver's average rating
driver_rating = carpool_group.get_driver_rating(driver_example)

# Print the names of the matched passengers and the driver's rating
print([passenger.name for passenger in matched_passengers], driver_rating)