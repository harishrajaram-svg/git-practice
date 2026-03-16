def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def main():
    operations = {'1': add, '2': subtract, '3': multiply, '4': divide}

    while True:
        print("\n--- Calculator Menu ---")
        print("1) Add")
        print("2) Subtract")
        print("3) Multiply")
        print("4) Divide")
        print("5) Quit")

        choice = input("Pick an operation (1-5): ")

        if choice == '5':
            print("Goodbye!")
            break

        if choice not in operations:
            print("Invalid choice. Please enter 1-5.")
            continue

        try:
            a = float(input("Enter first number: "))
            b = float(input("Enter second number: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        try:
            result = operations[choice](a, b)
            print(f"Result: {result}")
        except ValueError as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
