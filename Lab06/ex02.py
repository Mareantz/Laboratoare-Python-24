# Design a bank account system with a base class Account and subclasses SavingsAccount and CheckingAccount. Implement
# methods for deposit, withdrawal, and interest calculation.

class Account:
    def __init__(self, account_number, balance=0):
        self.account_number = account_number
        self.balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"Deposited {amount}. New balance: {self.balance}")
        else:
            print("Deposit amount must be positive.")

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            print(f"Withdrew {amount}. New balance: {self.balance}")
        else:
            print("Insufficient balance or invalid amount.")

    def display_balance(self):
        print(f"Account {self.account_number} balance: {self.balance}")


class SavingsAccount(Account):
    def __init__(self, account_number, balance=0, interest_rate=0.02):
        super().__init__(account_number, balance)
        self.interest_rate = interest_rate

    def calculate_interest(self):
        interest = self.balance * self.interest_rate
        print(f"Interest for account {self.account_number} is {interest}")
        return interest


class CheckingAccount(Account):
    def __init__(self, account_number, balance=0, overdraft_limit=100):
        super().__init__(account_number, balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        if amount > 0 and (self.balance - amount >= -self.overdraft_limit):
            self.balance -= amount
            print(f"Withdrew {amount}. New balance: {self.balance}")
        else:
            print("Withdrawal exceeds overdraft limit or invalid amount.")

    def display_overdraft_limit(self):
        print(f"Account {self.account_number} overdraft limit: {self.overdraft_limit}")


if __name__ == "__main__":
    savings = SavingsAccount(account_number="S123", balance=1000, interest_rate=0.03)
    savings.deposit(500)
    savings.withdraw(300)
    savings.calculate_interest()
    savings.display_balance()

    checking = CheckingAccount(account_number="C123", balance=500, overdraft_limit=200)
    checking.deposit(200)
    checking.withdraw(800)
    checking.display_balance()
    checking.display_overdraft_limit()
