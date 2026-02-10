"""
File name format required:
matricula_ApellidoNombre.py
Example: 1030034_CarlosTovar.py

Note: Code, variables, functions, and outputs are in English (as requested).
Comments can be in Spanish.
"""


# --------------------------------------------------
# Problem 1: Rectangle area and perimeter (basic functions)
# Description: This program calculates the area and perimeter of a rectangle
#              using two separate functions. The main code validates inputs
#              before calling the functions and prints the results.
#
# Inputs:
# - width (float)
# - height (float)
#
# Outputs:
# - "Area:" <area_value>
# - "Perimeter:" <perimeter_value>
#
# Validations:
# - width > 0
# - height > 0
# - If invalid: print "Error: invalid input" and do NOT call the functions.
#
# Test cases:
# 1) Normal: width=5.0, height=3.0
# 2) Edge case: width=0.0001, height=0.0001
# 3) Error: width=-2.0, height=4.0
# --------------------------------------------------
def calculate_area(width: float, height: float) -> float:
    return width * height


def calculate_perimeter(width: float, height: float) -> float:
    return 2 * (width + height)


def run_problem_1(width: float, height: float) -> None:
    if width <= 0 or height <= 0:
        print("Error: invalid input")
        return

    area_value = calculate_area(width, height)
    perimeter_value = calculate_perimeter(width, height)

    print(f"Area: {area_value}")
    print(f"Perimeter: {perimeter_value}")


# --------------------------------------------------
# Problem 2: Grade classifier (function with return string)
# Description: This program classifies a numeric score (0-100) into a letter
#              grade category using a function. The main code validates the
#              score before calling the function.
#
# Inputs:
# - score (int or float)
#
# Outputs:
# - "Score:" <score>
# - "Category:" <grade_letter>
#
# Validations:
# - 0 <= score <= 100
# - If invalid: print "Error: invalid input" and do NOT classify.
#
# Test cases:
# 1) Normal: score=85
# 2) Edge case: score=100
# 3) Error: score=120
# --------------------------------------------------
def classify_grade(score: float) -> str:
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    if score >= 60:
        return "D"
    return "F"


def run_problem_2(score) -> None:
    if not isinstance(score, (int, float)) or score < 0 or score > 100:
        print("Error: invalid input")
        return

    category = classify_grade(float(score))
    print(f"Score: {score}")
    print(f"Category: {category}")


# --------------------------------------------------
# Problem 3: List statistics function (min, max, average)
# Description: This program reads a comma-separated string of numbers,
#              converts it into a list, and summarizes min, max, and average
#              using a function that returns a dictionary.
#
# Inputs:
# - numbers_text (string; e.g., "10,20,30")
# - Internally: numbers_list (list of float)
#
# Outputs:
# - "Min:" <min_value>
# - "Max:" <max_value>
# - "Average:" <average_value>
#
# Validations:
# - numbers_text is not empty after strip()
# - list is not empty after conversion
# - all elements must be convertible to numbers
# - If invalid: print "Error: invalid input"
#
# Test cases:
# 1) Normal: "10, 20, 30"
# 2) Edge case: "7"
# 3) Error: "10, abc, 30"
# --------------------------------------------------
def summarize_numbers(numbers_list: list[float]) -> dict:
    return {
        "min": min(numbers_list),
        "max": max(numbers_list),
        "average": sum(numbers_list) / len(numbers_list),
    }


def parse_numbers_text(numbers_text: str) -> list[float] | None:
    if not isinstance(numbers_text, str):
        return None

    cleaned = numbers_text.strip()
    if cleaned == "":
        return None

    parts = [p.strip() for p in cleaned.split(",")]
    numbers: list[float] = []

    for part in parts:
        if part == "":
            return None
        try:
            numbers.append(float(part))
        except ValueError:
            return None

    return numbers if len(numbers) > 0 else None


def run_problem_3(numbers_text: str) -> None:
    numbers_list = parse_numbers_text(numbers_text)
    if numbers_list is None or len(numbers_list) == 0:
        print("Error: invalid input")
        return

    summary = summarize_numbers(numbers_list)
    print(f"Min: {summary['min']}")
    print(f"Max: {summary['max']}")
    print(f"Average: {summary['average']}")


# --------------------------------------------------
# Problem 4: Apply discount list (pure function)
# Description: This program applies a discount rate to a list of prices.
#              The function returns a NEW list (pure function) without
#              modifying the original list.
#
# Inputs:
# - prices_text (string; e.g., "100,200,300")
# - discount_rate (float between 0 and 1)
#
# Outputs:
# - "Original prices:" <original_list>
# - "Discounted prices:" <discounted_list>
#
# Validations:
# - prices_text not empty, list not empty
# - all prices > 0
# - 0 <= discount_rate <= 1
# - If invalid: print "Error: invalid input"
#
# Test cases:
# 1) Normal: prices_text="100, 200, 300", discount_rate=0.10
# 2) Edge case: prices_text="1", discount_rate=0
# 3) Error: prices_text="100, -50, 200", discount_rate=0.20
# --------------------------------------------------
def apply_discount(prices_list: list[float], discount_rate: float) -> list[float]:
    discounted_list: list[float] = []
    for price in prices_list:
        discounted_price = price * (1 - discount_rate)
        discounted_list.append(discounted_price)
    return discounted_list


def parse_prices_text(prices_text: str) -> list[float] | None:
    # Same logic as numbers, but later we validate > 0
    return parse_numbers_text(prices_text)


def run_problem_4(prices_text: str, discount_rate) -> None:
    if not isinstance(discount_rate, (int, float)):
        print("Error: invalid input")
        return

    discount_rate = float(discount_rate)
    if discount_rate < 0 or discount_rate > 1:
        print("Error: invalid input")
        return

    prices_list = parse_prices_text(prices_text)
    if prices_list is None or len(prices_list) == 0:
        print("Error: invalid input")
        return

    if any(price <= 0 for price in prices_list):
        print("Error: invalid input")
        return

    discounted_list = apply_discount(prices_list, discount_rate)
    print(f"Original prices: {prices_list}")
    print(f"Discounted prices: {discounted_list}")


# --------------------------------------------------
# Problem 5: Greeting function with default parameters
# Description: This program generates a greeting using a function with a
#              default parameter. If a title is provided, it is placed before
#              the name with exactly one space.
#
# Inputs:
# - name (string)
# - title (string optional)
#
# Outputs:
# - "Greeting:" <greeting_message>
#
# Validations:
# - name not empty after strip()
# - title can be empty, but if not empty it is also stripped
# - If invalid: print "Error: invalid input"
#
# Test cases:
# 1) Normal: name="Alice", title="Dr."
# 2) Edge case: name="Bob", title=""
# 3) Error: name="   ", title="Eng."
# --------------------------------------------------
def greet(name: str, title: str = "") -> str:
    cleaned_name = name.strip()
    cleaned_title = title.strip()

    full_name = cleaned_name
    if cleaned_title != "":
        full_name = f"{cleaned_title} {cleaned_name}"

    return f"Hello, {full_name}!"


def run_problem_5(name: str, title: str = "") -> None:
    if not isinstance(name, str) or not isinstance(title, str):
        print("Error: invalid input")
        return

    if name.strip() == "":
        print("Error: invalid input")
        return

    message = greet(name, title=title)  # named argument usage
    print(f"Greeting: {message}")


# --------------------------------------------------
# Problem 6: Factorial function (iterative)
# Description: This program computes n! using an iterative approach (for loop).
#              Iterative was chosen to avoid recursion depth issues and keep
#              the implementation straightforward.
#
# Inputs:
# - n (int)
#
# Outputs:
# - "n:" <n>
# - "Factorial:" <factorial_value>
#
# Validations:
# - n must be int
# - n >= 0
# - Optional: n <= 20 (to keep numbers manageable)
# - If invalid: print "Error: invalid input" and do NOT call factorial()
#
# Test cases:
# 1) Normal: n=5
# 2) Edge case: n=0
# 3) Error: n=-3
# --------------------------------------------------
MAX_FACTORIAL_N = 20


def factorial(n: int) -> int:
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result


def run_problem_6(n) -> None:
    if not isinstance(n, int) or n < 0 or n > MAX_FACTORIAL_N:
        print("Error: invalid input")
        return

    fact_value = factorial(n)
    print(f"n: {n}")
    print(f"Factorial: {fact_value}")


# --------------------------------------------------
# Main code: calls each problem using the 3 required test cases
# --------------------------------------------------
def main() -> None:
    print("=== Problem 1 Tests ===")
    run_problem_1(5.0, 3.0)          # Normal
    run_problem_1(0.0001, 0.0001)    # Edge
    run_problem_1(-2.0, 4.0)         # Error
    print()

    print("=== Problem 2 Tests ===")
    run_problem_2(85)                # Normal
    run_problem_2(100)               # Edge
    run_problem_2(120)               # Error
    print()

    print("=== Problem 3 Tests ===")
    run_problem_3("10, 20, 30")      # Normal
    run_problem_3("7")               # Edge
    run_problem_3("10, abc, 30")     # Error
    print()

    print("=== Problem 4 Tests ===")
    run_problem_4("100, 200, 300", 0.10)   # Normal
    run_problem_4("1", 0)                  # Edge
    run_problem_4("100, -50, 200", 0.20)   # Error
    print()

    print("=== Problem 5 Tests ===")
    run_problem_5("Alice", "Dr.")          # Normal
    run_problem_5("Bob")                   # Edge (default title)
    run_problem_5("   ", "Eng.")           # Error
    print()

    print("=== Problem 6 Tests ===")
    run_problem_6(5)                       # Normal
    run_problem_6(0)                       # Edge
    run_problem_6(-3)                      # Error


if __name__ == "__main__":
    main()

