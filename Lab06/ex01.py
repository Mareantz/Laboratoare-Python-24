# Create a class hierarchy for shapes, starting with a base class Shape. Then, create subclasses like Circle,
# Rectangle, and Triangle. Implement methods to calculate area and perimeter for each shape.

from math import pi, sqrt


class Shape:
    def area(self):
        raise NotImplementedError("Subclasses must implement this method")

    def perimeter(self):
        raise NotImplementedError("Subclasses must implement this method")


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return pi * self.radius ** 2

    def perimeter(self):
        return 2 * pi * self.radius


class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)


class Triangle(Shape):
    def __init__(self, side1, side2, side3):
        self.side1 = side1
        self.side2 = side2
        self.side3 = side3

    def area(self):
        s = self.perimeter() / 2
        return sqrt(s * (s - self.side1) * (s - self.side2) * (s - self.side3))

    def perimeter(self):
        return self.side1 + self.side2 + self.side3


if __name__ == "__main__":
    circle = Circle(radius=5)
    print(f"Circle - Area: {circle.area()}, Perimeter: {circle.perimeter()}")

    rectangle = Rectangle(width=4, height=7)
    print(f"Rectangle - Area: {rectangle.area()}, Perimeter: {rectangle.perimeter()}")

    triangle = Triangle(side1=3, side2=4, side3=5)
    print(f"Triangle - Area: {triangle.area()}, Perimeter: {triangle.perimeter()}")
