# Create a class hierarchy for animals, starting with a base class Animal. Then, create subclasses like Mammal, Bird,
# and Fish. Add properties and methods to represent characteristics unique to each animal group.

class Animal:
    def __init__(self, name, habitat, diet):
        self.name = name
        self.habitat = habitat
        self.diet = diet

    def display_info(self):
        print(f"Name: {self.name}, Habitat: {self.habitat}, Diet: {self.diet}")

    def make_sound(self):
        raise NotImplementedError("Subclasses must implement this method")


class Mammal(Animal):
    def __init__(self, name, habitat, diet, fur_color):
        super().__init__(name, habitat, diet)
        self.fur_color = fur_color

    def display_info(self):
        super().display_info()
        print(f"Fur Color: {self.fur_color}")

    def make_sound(self):
        print(f"{self.name} makes a growling sound.")

    def give_birth(self):
        print(f"{self.name} gives live birth.")


class Bird(Animal):
    def __init__(self, name, habitat, diet, wing_span):
        super().__init__(name, habitat, diet)
        self.wing_span = wing_span

    def display_info(self):
        super().display_info()
        print(f"Wing Span: {self.wing_span} meters")

    def make_sound(self):
        print(f"{self.name} sings or chirps.")

    def fly(self):
        print(f"{self.name} is flying with a wingspan of {self.wing_span} meters.")


class Fish(Animal):
    def __init__(self, name, habitat, diet, scale_type):
        super().__init__(name, habitat, diet)
        self.scale_type = scale_type

    def display_info(self):
        super().display_info()
        print(f"Scale Type: {self.scale_type}")

    def make_sound(self):
        print(f"{self.name} makes a bubbling sound.")

    def swim(self):
        print(f"{self.name} is swimming.")


if __name__ == "__main__":
    mammal = Mammal(name="Lion", habitat="Savannah", diet="Carnivore", fur_color="Golden")
    mammal.display_info()
    mammal.make_sound()
    mammal.give_birth()

    bird = Bird(name="Eagle", habitat="Mountains", diet="Carnivore", wing_span=2.5)
    bird.display_info()
    bird.make_sound()
    bird.fly()

    fish = Fish(name="Clownfish", habitat="Coral Reef", diet="Omnivore", scale_type="Smooth")
    fish.display_info()
    fish.make_sound()
    fish.swim()
