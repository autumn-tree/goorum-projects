"""
- Class definition
- Module-style organization
- Exception handling
"""

# class definition
class Calculator:
    """Simple calculator class"""

    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        try:
            return a / b
        except ZeroDivisionError:
            return "Cannot divide by zero"


# using calculator module
def main():
    """Main function acts as module execution entry"""
    calc = Calculator()

    print("Add:", calc.add(10, 5))
    print("Subtract:", calc.subtract(10, 5))
    print("Multiply:", calc.multiply(10, 5))
    print("Divide:", calc.divide(10, 0))


# execution
if __name__ == "__main__":
    main()
