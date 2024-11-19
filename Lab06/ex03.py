# Create a base class Vehicle with attributes like make, model, and year, and then create subclasses for specific
# types of vehicles like Car, Motorcycle, and Truck. Add methods to calculate mileage or towing capacity based on the
# vehicle type.

class Vehicle:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year

    def display_info(self):
        print(f"{self.year} {self.make} {self.model}")

    def calculate_mileage(self):
        raise NotImplementedError("This method must be overridden by subclasses")


class Car(Vehicle):
    def __init__(self, make, model, year, mpg):
        super().__init__(make, model, year)
        self.mpg = mpg

    def calculate_mileage(self, miles_driven, gallons_used):
        mileage = miles_driven / gallons_used
        print(f"Car mileage: {mileage:.2f} MPG (Expected MPG: {self.mpg})")
        return mileage


class Motorcycle(Vehicle):
    def __init__(self, make, model, year, mpg):
        super().__init__(make, model, year)
        self.mpg = mpg

    def calculate_mileage(self, miles_driven, gallons_used):
        mileage = miles_driven / gallons_used
        print(f"Motorcycle mileage: {mileage:.2f} MPG (Expected MPG: {self.mpg})")
        return mileage


class Truck(Vehicle):
    def __init__(self, make, model, year, towing_capacity):
        super().__init__(make, model, year)
        self.towing_capacity = towing_capacity

    def calculate_towing_capacity(self, weight):
        if weight <= self.towing_capacity:
            print(f"The truck can tow {weight} lbs (Max: {self.towing_capacity} lbs).")
        else:
            print(f"The truck cannot tow {weight} lbs. Exceeds capacity of {self.towing_capacity} lbs.")


if __name__ == "__main__":
    car = Car(make="Toyota", model="Camry", year=2021, mpg=30)
    car.display_info()
    car.calculate_mileage(miles_driven=300, gallons_used=10)

    motorcycle = Motorcycle(make="Harley-Davidson", model="Street 750", year=2019, mpg=55)
    motorcycle.display_info()
    motorcycle.calculate_mileage(miles_driven=220, gallons_used=4)

    truck = Truck(make="Ford", model="F-150", year=2022, towing_capacity=13000)
    truck.display_info()
    truck.calculate_towing_capacity(weight=12000)
    truck.calculate_towing_capacity(weight=14000)
