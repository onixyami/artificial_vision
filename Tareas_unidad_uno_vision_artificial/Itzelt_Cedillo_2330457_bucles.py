MAX_ATTEMPTS = 3
CORRECT_PASSWORD = "admin123"
SENTINEL_VALUE = -1.0


def read_int(prompt: str):
    """Safely read an int from input. Returns int or None if invalid."""
    raw_value = input(prompt).strip()
    try:
        return int(raw_value)
    except ValueError:
        return None


def read_float(prompt: str):
    """Safely read a float from input. Returns float or None if invalid."""
    raw_value = input(prompt).strip()
    try:
        return float(raw_value)
    except ValueError:
        return None


# ----------------------------------------------------------
# Problem 1: Sum of integers in a range
# Description: Calculates the sum of all integers from 1 to n (inclusive).
#              Also calculates the sum of only the even numbers in the same range,
#              using a for loop with range().
#
# Inputs:
# - n (int): upper limit of the range.
#
# Outputs:
# - "Sum 1..n:" <total_sum>
# - "Even sum 1..n:" <even_sum>
#
# Validations:
# - n must be convertible to int.
# - n >= 1; otherwise print "Error: invalid input".
#
# Test cases:
# 1) Normal: n = 10  -> Sum 1..n: 55, Even sum 1..n: 30
# 2) Edge case: n = 1 -> Sum 1..n: 1, Even sum 1..n: 0
# 3) Error: n = "abc" or n = 0 -> Error: invalid input
# ----------------------------------------------------------
def problem_1_sum_range():
    print("\n--- Problem 1: Sum of integers in a range ---")
    n = read_int("Enter n (int, n >= 1): ")

    if n is None or n < 1:
        print("Error: invalid input")
        return

    total_sum = 0
    even_sum = 0

    for value in range(1, n + 1):
        total_sum = total_sum + value
        if value % 2 == 0:
            even_sum = even_sum + value

    print(f"Sum 1..n: {total_sum}")
    print(f"Even sum 1..n: {even_sum}")


# ----------------------------------------------------------
# Problem 2: Multiplication table with for
# Description: Prints the multiplication table of a base number from 1 to m.
#              Uses a for loop with range() and f-strings.
#
# Inputs:
# - base (int)
# - m (int): table limit
#
# Outputs:
# - "base x i = product" for i in 1..m
#
# Validations:
# - base and m must be convertible to int.
# - m >= 1; otherwise print "Error: invalid input".
#
# Test cases:
# 1) Normal: base = 5, m = 4 -> prints 5 x 1..4
# 2) Edge case: base = 0, m = 1 -> "0 x 1 = 0"
# 3) Error: base = "x" or m = 0 -> Error: invalid input
# ----------------------------------------------------------
def problem_2_multiplication_table():
    print("\n--- Problem 2: Multiplication table with for ---")
    base = read_int("Enter base (int): ")
    m = read_int("Enter m (int, m >= 1): ")

    if base is None or m is None or m < 1:
        print("Error: invalid input")
        return

    for i in range(1, m + 1):
        product = base * i
        print(f"{base} x {i} = {product}")


# ----------------------------------------------------------
# Problem 3: Average of numbers with while and sentinel
# Description: Reads numbers until the sentinel value is entered (-1 by default).
#              Accepts only numbers >= 0 as valid data.
#              Rejects negative numbers other than the sentinel.
#              Computes count and average of valid inputs.
#
# Inputs:
# - number (float): repeated input
# - sentinel_value: fixed constant in code (SENTINEL_VALUE)
#
# Outputs:
# - "Count:" <count>
# - "Average:" <average_value>
# - If no valid data: "Error: no data"
#
# Validations:
# - Each input must be convertible to float; otherwise:
#   print "Error: invalid input" and ask again (do not count it).
# - Ignore sentinel in calculations.
#
# Test cases:
# 1) Normal: 10, 20, 30, -1 -> Count: 3, Average: 20.0
# 2) Edge case: -1 -> Error: no data
# 3) Error: "hello" then 5 then -1 -> invalid input message, then Count: 1, Average: 5.0
# ----------------------------------------------------------
def problem_3_average_with_sentinel():
    print("\n--- Problem 3: Average of numbers with while and sentinel ---")
    print(f"Enter numbers (float). Type {SENTINEL_VALUE} to finish.")

    count = 0
    total_sum = 0.0

    while True:
        number = read_float("Enter number: ")

        if number is None:
            print("Error: invalid input")
            continue

        if number == SENTINEL_VALUE:
            break

        if number < 0:
            print("Error: invalid input")
            continue

        total_sum = total_sum + number
        count = count + 1

    if count == 0:
        print("Error: no data")
        return

    average_value = total_sum / count
    print(f"Count: {count}")
    print(f"Average: {average_value}")


# ----------------------------------------------------------
# Problem 4: Password attempts with while
# Description: Simple password attempt system. User has MAX_ATTEMPTS attempts
#              to enter the correct password (exact match, case-sensitive).
#
# Inputs:
# - user_password (string): repeated input
#
# Outputs:
# - "Login success" if correct within limit
# - "Account locked" if all attempts are used
#
# Validations:
# - MAX_ATTEMPTS must be > 0 (constant in code).
# - Count attempts correctly.
#
# Test cases:
# 1) Normal: correct on 2nd try -> Login success
# 2) Edge case: MAX_ATTEMPTS = 1 and correct -> Login success
# 3) Error: wrong password MAX_ATTEMPTS times -> Account locked
# ----------------------------------------------------------
def problem_4_password_attempts():
    print("\n--- Problem 4: Password attempts with while ---")

    if MAX_ATTEMPTS <= 0:
        print("Error: invalid input")
        return

    attempts = 0

    while attempts < MAX_ATTEMPTS:
        user_password = input("Enter password: ")
        if user_password == CORRECT_PASSWORD:
            print("Login success")
            return
        attempts = attempts + 1

    print("Account locked")


# ----------------------------------------------------------
# Problem 5: Simple menu with while
# Description: Repeats a text menu until the user selects exit (0).
#              Allows greeting, showing counter, incrementing counter.
#
# Inputs:
# - option (string or int): user choice
#
# Outputs:
# - "Hello!" for greeting
# - "Counter:" <counter_value> to show counter
# - "Counter incremented" when incrementing
# - "Bye!" on exit
# - "Error: invalid option" for invalid option or non-int input
#
# Validations:
# - Convert option to int safely; if not convertible, print error and continue.
# - Only accept 0, 1, 2, 3.
#
# Test cases:
# 1) Normal: 1, 3, 2, 0 -> greeting, increment, show, exit
# 2) Edge case: 0 -> Bye! immediately
# 3) Error: "abc", 9, 0 -> invalid option messages, then exit
# ----------------------------------------------------------
def problem_5_simple_menu():
    print("\n--- Problem 5: Simple menu with while ---")

    counter_value = 0
    option = -1

    while option != 0:
        print("\n1) Show greeting")
        print("2) Show current counter value")
        print("3) Increment counter")
        print("0) Exit")

        raw_option = input("Select an option: ").strip()

        try:
            option = int(raw_option)
        except ValueError:
            print("Error: invalid option")
            continue

        if option == 1:
            print("Hello!")
        elif option == 2:
            print(f"Counter: {counter_value}")
        elif option == 3:
            counter_value = counter_value + 1
            print("Counter incremented")
        elif option == 0:
            print("Bye!")
        else:
            print("Error: invalid option")


# ----------------------------------------------------------
# Problem 6: Pattern printing with nested loops
# Description: Prints a right triangle of asterisks with n rows using nested for loops.
#              Also prints an inverted triangle (extension included and documented here).
#
# Inputs:
# - n (int): number of rows
#
# Outputs:
# - Lines with increasing '*' from 1..n
# - Inverted pattern from n..1
#
# Validations:
# - n must be convertible to int.
# - n >= 1; otherwise print "Error: invalid input".
#
# Test cases:
# 1) Normal: n = 4 -> prints 4-line triangle and inverted triangle
# 2) Edge case: n = 1 -> prints "*" then "*"
# 3) Error: n = -2 or n = "hi" -> Error: invalid input
# ----------------------------------------------------------
def problem_6_pattern_printing():
    print("\n--- Problem 6: Pattern printing with nested loops ---")
    n = read_int("Enter n (int, n >= 1): ")

    if n is None or n < 1:
        print("Error: invalid input")
        return

    print("\nRight triangle:")
    for i in range(1, n + 1):
        line = ""
        for _ in range(i):
            line += "*"
        print(line)

    # Optional extension: inverted triangle (documented in Description/Outputs above)
    print("\nInverted triangle:")
    for i in range(n, 0, -1):
        line = ""
        for _ in range(i):
            line += "*"
        print(line)


def main():
    # Runs all 6 problems in order (single file delivery requirement).
    problem_1_sum_range()
    problem_2_multiplication_table()
    problem_3_average_with_sentinel()
    problem_4_password_attempts()
    problem_5_simple_menu()
    problem_6_pattern_printing()


if __name__ == "__main__":
    main()
