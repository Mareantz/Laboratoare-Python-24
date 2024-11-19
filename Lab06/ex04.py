# Build an employee hierarchy with a base class Employee. Create subclasses for different types of employees like
# Manager, Engineer, and Salesperson. Each subclass should have attributes like salary and methods related to their
# roles.

class Employee:
    def __init__(self, name, id_number, salary):
        self.name = name
        self.id_number = id_number
        self.salary = salary

    def display_info(self):
        print(f"Employee ID: {self.id_number}, Name: {self.name}, Salary: ${self.salary:.2f}")

    def calculate_annual_salary(self):
        return self.salary * 12


class Manager(Employee):
    def __init__(self, name, id_number, salary, team_size):
        super().__init__(name, id_number, salary)
        self.team_size = team_size

    def display_team_size(self):
        print(f"Manager {self.name} manages a team of {self.team_size} employees.")

    def calculate_bonus(self):
        bonus = self.salary * 0.1 * self.team_size
        print(f"Manager {self.name}'s bonus: ${bonus:.2f}")
        return bonus


class Engineer(Employee):
    def __init__(self, name, id_number, salary, specialty):
        super().__init__(name, id_number, salary)
        self.specialty = specialty

    def display_specialty(self):
        print(f"Engineer {self.name} specializes in {self.specialty}.")

    def calculate_project_bonus(self, projects_completed):
        bonus = 500 * projects_completed
        print(f"Engineer {self.name}'s bonus for completing {projects_completed} projects: ${bonus:.2f}")
        return bonus


class Salesperson(Employee):
    def __init__(self, name, id_number, salary, commission_rate):
        super().__init__(name, id_number, salary)
        self.commission_rate = commission_rate

    def calculate_commission(self, sales_amount):
        commission = sales_amount * (self.commission_rate / 100)
        print(f"Salesperson {self.name}'s commission for ${sales_amount:.2f} in sales: ${commission:.2f}")
        return commission


if __name__ == "__main__":
    manager = Manager(name="Alice", id_number="M001", salary=8000, team_size=5)
    manager.display_info()
    manager.display_team_size()
    manager.calculate_bonus()

    engineer = Engineer(name="Bob", id_number="E001", salary=6000, specialty="Software Development")
    engineer.display_info()
    engineer.display_specialty()
    engineer.calculate_project_bonus(projects_completed=3)

    salesperson = Salesperson(name="Charlie", id_number="S001", salary=4000, commission_rate=10)
    salesperson.display_info()
    salesperson.calculate_commission(sales_amount=20000)
