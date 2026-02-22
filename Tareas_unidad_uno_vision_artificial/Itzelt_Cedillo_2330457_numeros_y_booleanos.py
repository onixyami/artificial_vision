
ABSOLUTE_ZERO_C = -273.15
REGULAR_HOURS_LIMIT = 40
OVERTIME_MULTIPLIER = 1.5
DISCOUNT_RATE = 0.10


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


def parse_yes_no(prompt: str):
    """
    Reads YES/NO (case-insensitive). Returns bool or None if invalid.
    YES -> True, NO -> False
    """
    text_value = input(prompt).strip().upper()
    if text_value == "YES":
        return True
    if text_value == "NO":
        return False
    return None


# ----------------------------------------------------------
# Problem 1: Temperature converter and range flag
# Description: Converts a temperature from Celsius (float) to Fahrenheit and Kelvin.
#              Also computes a boolean flag is_high_temperature (>= 30.0 C).
#
# Inputs:
# - temp_c (float): temperature in Celsius.
#
# Outputs:
# - "Fahrenheit:" <temp_f>
# - "Kelvin:" <temp_k>
# - "High temperature:" True|False
#
# Validations:
# - temp_c must be convertible to float.
# - temp_c must be >= -273.15 (absolute zero) to avoid impossible Kelvin values.
#
# Test cases:
# 1) Normal: temp_c = 30.0 -> Fahrenheit 86.0, Kelvin 303.15, High temperature True
# 2) Edge case: temp_c = -273.15 -> Kelvin 0.0, High temperature False
# 3) Error: temp_c = -300 or "abc" -> Error: invalid input
# ----------------------------------------------------------
def problem_1_temperature_converter():
    print("\n--- Problem 1: Temperature converter and range flag ---")

    temp_c = read_float("Enter temperature in Celsius (float): ")
    if temp_c is None or temp_c < ABSOLUTE_ZERO_C:
        print("Error: invalid input")
        return

    temp_f = temp_c * 9 / 5 + 32
    temp_k = temp_c + 273.15
    is_high_temperature = (temp_c >= 30.0)

    print(f"Fahrenheit: {temp_f}")
    print(f"Kelvin: {temp_k}")
    print(f"High temperature: {is_high_temperature}")


# ----------------------------------------------------------
# Problem 2: Work hours and overtime payment
# Description: Computes weekly pay. Up to 40 hours are paid at hourly_rate.
#              Overtime hours (> 40) are paid at 150% rate. Also sets has_overtime.
#
# Inputs:
# - hours_worked (int): weekly hours worked
# - hourly_rate (float): pay per hour
#
# Outputs:
# - "Regular pay:" <regular_pay>
# - "Overtime pay:" <overtime_pay>
# - "Total pay:" <total_pay>
# - "Has overtime:" True|False
#
# Validations:
# - hours_worked >= 0
# - hourly_rate > 0
# - if invalid: "Error: invalid input"
#
# Test cases:
# 1) Normal: hours=45, rate=100.0 -> regular=4000, overtime=750, total=4750, has_overtime True
# 2) Edge case: hours=40, rate=50.0 -> overtime=0, has_overtime False
# 3) Error: hours=-1 or rate=0 -> Error: invalid input
# ----------------------------------------------------------
def problem_2_overtime_payment():
    print("\n--- Problem 2: Work hours and overtime payment ---")

    hours_worked = read_int("Enter hours worked (int, >= 0): ")
    hourly_rate = read_float("Enter hourly rate (float, > 0): ")

    if hours_worked is None or hourly_rate is None or hours_worked < 0 or hourly_rate <= 0:
        print("Error: invalid input")
        return

    regular_hours = min(hours_worked, REGULAR_HOURS_LIMIT)
    overtime_hours = max(hours_worked - REGULAR_HOURS_LIMIT, 0)

    regular_pay = regular_hours * hourly_rate
    overtime_pay = overtime_hours * hourly_rate * OVERTIME_MULTIPLIER
    total_pay = regular_pay + overtime_pay
    has_overtime = (hours_worked > REGULAR_HOURS_LIMIT)

    print(f"Regular pay: {regular_pay}")
    print(f"Overtime pay: {overtime_pay}")
    print(f"Total pay: {total_pay}")
    print(f"Has overtime: {has_overtime}")


# ----------------------------------------------------------
# Problem 3: Discount eligibility with booleans
# Description: Determines if a customer is eligible for a discount.
#              Eligible if is_student OR is_senior OR purchase_total >= 1000.0.
#              Applies a 10% discount if eligible.
#
# Inputs:
# - purchase_total (float)
# - is_student_text (string): "YES" or "NO"
# - is_senior_text (string): "YES" or "NO"
#
# Outputs:
# - "Discount eligible:" True|False
# - "Final total:" <final_total>
#
# Validations:
# - purchase_total must be convertible to float and >= 0.0
# - is_student_text and is_senior_text must be YES/NO (case-insensitive)
# - otherwise: "Error: invalid input"
#
# Test cases:
# 1) Normal: total=1200, student=NO, senior=NO -> eligible True, final 1080
# 2) Edge case: total=1000, student=NO, senior=NO -> eligible True, final 900
# 3) Error: student="MAYBE" or total=-5 -> Error: invalid input
# ----------------------------------------------------------
def problem_3_discount_eligibility():
    print("\n--- Problem 3: Discount eligibility with booleans ---")

    purchase_total = read_float("Enter purchase total (float, >= 0): ")
    if purchase_total is None or purchase_total < 0.0:
        print("Error: invalid input")
        return

    is_student = parse_yes_no("Is student? (YES/NO): ")
    is_senior = parse_yes_no("Is senior? (YES/NO): ")

    if is_student is None or is_senior is None:
        print("Error: invalid input")
        return

    discount_eligible = is_student or is_senior or (purchase_total >= 1000.0)

    if discount_eligible:
        final_total = purchase_total * (1 - DISCOUNT_RATE)
    else:
        final_total = purchase_total

    print(f"Discount eligible: {discount_eligible}")
    print(f"Final total: {final_total}")


# ----------------------------------------------------------
# Problem 4: Basic statistics of three integers
# Description: Reads three integers and computes sum, average (float),
#              maximum, minimum, and a boolean all_even flag.
#
# Inputs:
# - n1 (int)
# - n2 (int)
# - n3 (int)
#
# Outputs:
# - "Sum:" <sum_value>
# - "Average:" <average_value>
# - "Max:" <max_value>
# - "Min:" <min_value>
# - "All even:" True|False
#
# Validations:
# - each value must be convertible to int
#
# Test cases:
# 1) Normal: 2, 5, 9 -> Sum 16, Avg 5.333..., Max 9, Min 2, All even False
# 2) Edge case: 0, 0, 0 -> All even True
# 3) Error: n2="hi" -> Error: invalid input
# ----------------------------------------------------------
def problem_4_three_integers_stats():
    print("\n--- Problem 4: Basic statistics of three integers ---")

    n1 = read_int("Enter n1 (int): ")
    n2 = read_int("Enter n2 (int): ")
    n3 = read_int("Enter n3 (int): ")

    if n1 is None or n2 is None or n3 is None:
        print("Error: invalid input")
        return

    sum_value = n1 + n2 + n3
    average_value = sum_value / 3
    max_value = max(n1, n2, n3)
    min_value = min(n1, n2, n3)
    all_even = (n1 % 2 == 0) and (n2 % 2 == 0) and (n3 % 2 == 0)

    print(f"Sum: {sum_value}")
    print(f"Average: {average_value}")
    print(f"Max: {max_value}")
    print(f"Min: {min_value}")
    print(f"All even: {all_even}")


# ----------------------------------------------------------
# Problem 5: Loan eligibility (income and debt ratio)
# Description: Determines loan eligibility based on income, debt ratio,
#              and credit score. debt_ratio = monthly_debt / monthly_income.
#              Eligible if income >= 8000 AND ratio <= 0.4 AND score >= 650.
#
# Inputs:
# - monthly_income (float)
# - monthly_debt (float)
# - credit_score (int)
#
# Outputs:
# - "Debt ratio:" <debt_ratio>
# - "Eligible:" True|False
#
# Validations:
# - monthly_income > 0.0 (avoid division by zero)
# - monthly_debt >= 0.0
# - credit_score >= 0
# - if invalid: "Error: invalid input"
#
# Test cases:
# 1) Normal: income=10000, debt=3000, score=700 -> ratio 0.3, eligible True
# 2) Edge case: income=8000, debt=3200, score=650 -> ratio 0.4, eligible True
# 3) Error: income=0 or debt=-1 -> Error: invalid input
# ----------------------------------------------------------
def problem_5_loan_eligibility():
    print("\n--- Problem 5: Loan eligibility (income and debt ratio) ---")

    monthly_income = read_float("Enter monthly income (float, > 0): ")
    monthly_debt = read_float("Enter monthly debt (float, >= 0): ")
    credit_score = read_int("Enter credit score (int, >= 0): ")

    if (
        monthly_income is None or monthly_debt is None or credit_score is None
        or monthly_income <= 0.0 or monthly_debt < 0.0 or credit_score < 0
    ):
        print("Error: invalid input")
        return

    debt_ratio = monthly_debt / monthly_income
    eligible = (monthly_income >= 8000.0 and debt_ratio <= 0.4 and credit_score >= 650)

    print(f"Debt ratio: {debt_ratio}")
    print(f"Eligible: {eligible}")


# ----------------------------------------------------------
# Problem 6: Body Mass Index (BMI) and category flag
# Description: Computes BMI using bmi = weight_kg / (height_m^2).
#              Produces booleans:
#              - is_underweight (bmi < 18.5)
#              - is_normal (18.5 <= bmi < 25.0)
#              - is_overweight (bmi >= 25.0)
#              Exactly one should be True for valid inputs.
#
# Inputs:
# - weight_kg (float)
# - height_m (float)
#
# Outputs:
# - "BMI:" <bmi_rounded>
# - "Underweight:" True|False
# - "Normal:" True|False
# - "Overweight:" True|False
#
# Validations:
# - weight_kg > 0.0
# - height_m > 0.0
# - if invalid: "Error: invalid input"
#
# Test cases:
# 1) Normal: weight=70, height=1.75 -> BMI ~22.86, Normal True
# 2) Edge case: BMI exactly 18.5 (e.g., weight=53.9, height=1.71) -> Normal True
# 3) Error: height=0 or weight=-1 -> Error: invalid input
# ----------------------------------------------------------
def problem_6_bmi_category():
    print("\n--- Problem 6: Body Mass Index (BMI) and category flag ---")

    weight_kg = read_float("Enter weight in kg (float, > 0): ")
    height_m = read_float("Enter height in meters (float, > 0): ")

    if weight_kg is None or height_m is None or weight_kg <= 0.0 or height_m <= 0.0:
        print("Error: invalid input")
        return

    bmi = weight_kg / (height_m * height_m)
    bmi_rounded = round(bmi, 2)

    is_underweight = bmi < 18.5
    is_normal = (bmi >= 18.5) and (bmi < 25.0)
    is_overweight = bmi >= 25.0

    print(f"BMI: {bmi_rounded}")
    print(f"Underweight: {is_underweight}")
    print(f"Normal: {is_normal}")
    print(f"Overweight: {is_overweight}")


def main():
    # Runs all 6 problems in order (single file delivery requirement).
    problem_1_temperature_converter()
    problem_2_overtime_payment()
    problem_3_discount_eligibility()
    problem_4_three_integers_stats()
    problem_5_loan_eligibility()
    problem_6_bmi_category()


if __name__ == "__main__":
    main()
