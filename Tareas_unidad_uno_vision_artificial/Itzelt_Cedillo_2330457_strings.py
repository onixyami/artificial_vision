
MIN_PALINDROME_LENGTH = 3
LABEL_TOTAL_LENGTH = 30
MIN_PASSWORD_LENGTH = 8


def read_positive_float(prompt: str):
    """Safely read a positive float. Returns float or None if invalid."""
    raw_value = input(prompt).strip()
    try:
        value = float(raw_value)
    except ValueError:
        return None
    if value <= 0:
        return None
    return value


def normalize_spaces(text: str) -> str:
    """Strip and collapse multiple spaces into single spaces."""
    parts = text.strip().split()
    return " ".join(parts)


# ----------------------------------------------------------
# Problem 1: Full name formatter (name + initials)
# Description: Reads a full name string, normalizes spaces and casing,
#              prints the name in Title Case and prints initials like X.X.X.
#
# Inputs:
# - full_name (string): may include extra spaces and mixed casing
#
# Outputs:
# - "Formatted name: <Title Case Name>"
# - "Initials: <X.X.X.>"
#
# Validation:
# - full_name must not be empty after strip()
# - must contain at least 2 words (e.g., first name and last name)
#
# Test cases:
# 1) Normal: "juan carlos tovar" -> "Juan Carlos Tovar", "J.C.T."
# 2) Edge case: "  aNa  tOrRes  " -> "Ana Torres", "A.T."
# 3) Error: "   " or "juan" -> Error: invalid input
# ----------------------------------------------------------
def problem_1_full_name_formatter():
    print("\n--- Problem 1: Full name formatter ---")

    full_name = input("Enter full name: ")
    normalized = normalize_spaces(full_name)

    if normalized == "":
        print("Error: invalid input")
        return

    name_parts = normalized.split(" ")
    if len(name_parts) < 2:
        print("Error: invalid input")
        return

    formatted_name = normalized.title()

    initials = ""
    for part in name_parts:
        if part != "":
            initials += part[0].upper() + "."

    print(f"Formatted name: {formatted_name}")
    print(f"Initials: {initials}")


# ----------------------------------------------------------
# Problem 2: Simple email validator (structure + domain)
# Description: Validates a basic email format:
#              - exactly one '@'
#              - at least one '.' after '@'
#              - no spaces
#              If valid, prints the domain (part after '@').
#
# Inputs:
# - email_text (string)
#
# Outputs:
# - "Valid email: True|False"
# - If valid: "Domain: <domain_part>"
#
# Validation:
# - email_text must not be empty after strip()
# - must contain exactly one '@'
# - must not contain spaces
# - after '@', there must be at least one '.'
#
# Test cases:
# 1) Normal: "user@mail.com" -> Valid True, Domain mail.com
# 2) Edge case: "a@b.co" -> Valid True, Domain b.co
# 3) Error: "user@@mail.com" or "user@mailcom" or "user mail@x.com" -> Valid False
# ----------------------------------------------------------
def problem_2_email_validator():
    print("\n--- Problem 2: Simple email validator ---")

    email_text = input("Enter email: ").strip()

    if email_text == "":
        print("Error: invalid input")
        return

    if " " in email_text:
        print("Valid email: False")
        return

    at_count = email_text.count("@")
    if at_count != 1:
        print("Valid email: False")
        return

    at_index = email_text.find("@")
    domain_part = email_text[at_index + 1:]

    # domain must not be empty and must contain at least one dot
    if domain_part == "" or "." not in domain_part:
        print("Valid email: False")
        return

    # basic structure: also ensure something exists before '@'
    local_part = email_text[:at_index]
    if local_part == "":
        print("Valid email: False")
        return

    print("Valid email: True")
    print(f"Domain: {domain_part}")


# ----------------------------------------------------------
# Problem 3: Palindrome checker (ignoring spaces and case)
# Description: Checks if a phrase is a palindrome ignoring spaces and case.
#              Uses lowercase + remove spaces, then compares with reversed text.
#
# Inputs:
# - phrase (string)
#
# Outputs:
# - "Is palindrome: True|False"
# - (Optional) "Normalized: <normalized_phrase>"
#
# Validation:
# - phrase must not be empty after strip()
# - after removing spaces, length must be at least 3 characters
#
# Test cases:
# 1) Normal: "Anita lava la tina" -> True
# 2) Edge case: "A a a" -> normalized "aaa" -> True
# 3) Error: "  " or "ab" -> Error: invalid input
# ----------------------------------------------------------
def problem_3_palindrome_checker():
    print("\n--- Problem 3: Palindrome checker ---")

    phrase = input("Enter a phrase: ")
    normalized_phrase = normalize_spaces(phrase).lower().replace(" ", "")

    if normalized_phrase == "" or len(normalized_phrase) < MIN_PALINDROME_LENGTH:
        print("Error: invalid input")
        return

    reversed_phrase = normalized_phrase[::-1]
    is_palindrome = (normalized_phrase == reversed_phrase)

    print(f"Is palindrome: {is_palindrome}")
    print(f"Normalized: {normalized_phrase}")


# ----------------------------------------------------------
# Problem 4: Sentence word statistics (lengths and first/last word)
# Description: Reads a sentence, normalizes spaces, splits into words,
#              and prints word count, first/last word, shortest and longest word.
#
# Inputs:
# - sentence (string)
#
# Outputs:
# - "Word count: <n>"
# - "First word: <...>"
# - "Last word: <...>"
# - "Shortest word: <...>"
# - "Longest word: <...>"
#
# Validation:
# - sentence must not be empty after strip()
# - after split(), must contain at least one word
#
# Test cases:
# 1) Normal: "Python is really fun" -> count 4, first Python, last fun
# 2) Edge case: "   hello   " -> count 1, first=last=shortest=longest=hello
# 3) Error: "   " -> Error: invalid input
# ----------------------------------------------------------
def problem_4_sentence_statistics():
    print("\n--- Problem 4: Sentence word statistics ---")

    sentence = input("Enter a sentence: ")
    normalized = normalize_spaces(sentence)

    if normalized == "":
        print("Error: invalid input")
        return

    words = normalized.split(" ")
    if len(words) == 0:
        print("Error: invalid input")
        return

    shortest_word = words[0]
    longest_word = words[0]

    for word in words:
        if len(word) < len(shortest_word):
            shortest_word = word
        if len(word) > len(longest_word):
            longest_word = word

    print(f"Word count: {len(words)}")
    print(f"First word: {words[0]}")
    print(f"Last word: {words[-1]}")
    print(f"Shortest word: {shortest_word}")
    print(f"Longest word: {longest_word}")


# ----------------------------------------------------------
# Problem 5: Password strength classifier
# Description: Classifies a password as weak/medium/strong using rules:
#              - Weak: length < 8 OR missing both upper+lower OR very simple
#              - Medium: length >= 8 and has at least two of: upper, lower, digit
#              - Strong: length >= 8 and has upper, lower, digit, and symbol
#              (symbol = any non-alphanumeric character)
#
# Inputs:
# - password_input (string)
#
# Outputs:
# - "Password strength: weak|medium|strong"
#
# Validation:
# - password must not be empty after strip()
# - length checked with len()
#
# Test cases:
# 1) Normal: "Abcdef1!" -> strong
# 2) Edge case: "Abcdef12" -> medium (no symbol)
# 3) Error: "" or "   " -> Error: invalid input
# ----------------------------------------------------------
def problem_5_password_strength():
    print("\n--- Problem 5: Password strength classifier ---")

    password_input = input("Enter password: ").strip()
    if password_input == "":
        print("Error: invalid input")
        return

    has_upper = False
    has_lower = False
    has_digit = False
    has_symbol = False

    for ch in password_input:
        if ch.isupper():
            has_upper = True
        elif ch.islower():
            has_lower = True
        elif ch.isdigit():
            has_digit = True
        elif not ch.isalnum():
            has_symbol = True

    length_ok = len(password_input) >= MIN_PASSWORD_LENGTH

    if length_ok and has_upper and has_lower and has_digit and has_symbol:
        strength = "strong"
    elif length_ok and ((has_upper and has_lower) or (has_lower and has_digit) or (has_upper and has_digit)):
        strength = "medium"
    else:
        strength = "weak"

    print(f"Password strength: {strength}")


# ----------------------------------------------------------
# Problem 6: Product label formatter (fixed-width text)
# Description: Builds a label line with this base format:
#              "Product: <NAME> | Price: $<PRICE>"
#              The final label must have exactly 30 characters:
#              - if shorter: pad with spaces
#              - if longer: cut to 30 characters
#
# Inputs:
# - product_name (string)
# - price_value (numeric text): must be convertible to a positive number
#
# Outputs:
# - "Label: "<exactly 30 characters>""
#
# Validation:
# - product_name must not be empty after strip()
# - price_value must be convertible to float and > 0
#
# Test cases:
# 1) Normal: name="Milk", price="25.5" -> label length 30
# 2) Edge case: name="A", price="0.01" -> label padded to 30
# 3) Error: name="  " or price="-5" or price="abc" -> Error: invalid input
# ----------------------------------------------------------
def problem_6_fixed_width_label():
    print("\n--- Problem 6: Product label formatter ---")

    product_name = input("Enter product name: ").strip()
    if product_name == "":
        print("Error: invalid input")
        return

    price_value = read_positive_float("Enter price (positive number): ")
    if price_value is None:
        print("Error: invalid input")
        return

    price_text = str(price_value)
    base_label = f"Product: {product_name} | Price: ${price_text}"

    if len(base_label) < LABEL_TOTAL_LENGTH:
        spaces_needed = LABEL_TOTAL_LENGTH - len(base_label)
        final_label = base_label + (" " * spaces_needed)
    else:
        final_label = base_label[:LABEL_TOTAL_LENGTH]

    print(f'Label: "{final_label}"')
    print(f"Length: {len(final_label)}")


def main():
    # Runs all 6 problems in order (single file delivery requirement).
    problem_1_full_name_formatter()
    problem_2_email_validator()
    problem_3_palindrome_checker()
    problem_4_sentence_statistics()
    problem_5_password_strength()
    problem_6_fixed_width_label()


if __name__ == "__main__":
    main()
