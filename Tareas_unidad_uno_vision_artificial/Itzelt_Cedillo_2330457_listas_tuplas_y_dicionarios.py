

PUNCTUATION_CHARS = ".,!?;:()[]{}\"'"


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


def normalize_item_name(text: str) -> str:
    """Normalize a product/item name for storage and search."""
    return text.strip().lower()


def remove_basic_punctuation(text: str) -> str:
    """Remove basic punctuation by replacing each punctuation char with space."""
    cleaned = text
    for ch in PUNCTUATION_CHARS:
        cleaned = cleaned.replace(ch, " ")
    return cleaned


# ----------------------------------------------------------
# Problem 1: Shopping list basics (list operations)
# Description: Parses an initial text into a shopping list (product names).
#              Allows adding a new product, shows list length, and checks if a
#              given product is in the list. All items are stored and searched
#              in lowercase for consistency.
#
# Inputs:
# - initial_items_text (string): e.g., "apple:2,banana:5,orange:6"
# - new_item (string): product to add
# - search_item (string): product to search
#
# Outputs:
# - "Items list:" <items_list>
# - "Total items:" <len_list>
# - "Found item:" True|False
#
# Validations:
# - initial_items_text must not be empty after strip()
# - split by commas; strip each part; allow formats like "name:qty"
# - new_item and search_item must not be empty after strip()
# - Decision: if the parsed list ends empty, treat it as invalid input
#
# Test cases:
# 1) Normal: "apple:2, banana:5, orange:6", new="milk", search="banana" -> Found True
# 2) Edge case: "apple:1", new="APPLE", search="apple" -> Found True (case-insensitive)
# 3) Error: initial_items_text="" or new_item="" -> Error: invalid input
# ----------------------------------------------------------
def problem_1_shopping_list():
    print("\n--- Problem 1: Shopping list basics ---")

    initial_items_text = input("Enter initial items text (e.g., apple:2,banana:5): ").strip()
    new_item = input("Enter new item to add: ").strip()
    search_item = input("Enter item to search: ").strip()

    if initial_items_text == "" or new_item == "" or search_item == "":
        print("Error: invalid input")
        return

    parts = initial_items_text.split(",")
    items_list = []

    for part in parts:
        part_clean = part.strip()
        if part_clean == "":
            continue

        # Accept "name:qty" or just "name"
        if ":" in part_clean:
            name_part = part_clean.split(":", 1)[0].strip()
        else:
            name_part = part_clean.strip()

        if name_part != "":
            items_list.append(normalize_item_name(name_part))

    # Decision documented in Validations: empty parsed list is invalid
    if len(items_list) == 0:
        print("Error: invalid input")
        return

    new_item_norm = normalize_item_name(new_item)
    items_list.append(new_item_norm)

    search_item_norm = normalize_item_name(search_item)
    is_in_list = search_item_norm in items_list

    print(f"Items list: {items_list}")
    print(f"Total items: {len(items_list)}")
    print(f"Found item: {is_in_list}")


# ----------------------------------------------------------
# Problem 2: Points and distances with tuples
# Description: Uses tuples to represent two 2D points (x, y).
#              Computes Euclidean distance and midpoint, outputting all results.
#
# Inputs:
# - x1, y1, x2, y2 (float)
#
# Outputs:
# - "Point A:" (x1, y1)
# - "Point B:" (x2, y2)
# - "Distance:" <distance>
# - "Midpoint:" (mx, my)
#
# Validations:
# - all 4 inputs must be convertible to float
#
# Test cases:
# 1) Normal: (0,0) and (3,4) -> Distance 5.0, Midpoint (1.5, 2.0)
# 2) Edge case: same points (2,2) and (2,2) -> Distance 0.0, Midpoint (2.0, 2.0)
# 3) Error: x1="hi" -> Error: invalid input
# ----------------------------------------------------------
def problem_2_points_tuples():
    print("\n--- Problem 2: Points and distances with tuples ---")

    x1 = read_float("Enter x1: ")
    y1 = read_float("Enter y1: ")
    x2 = read_float("Enter x2: ")
    y2 = read_float("Enter y2: ")

    if x1 is None or y1 is None or x2 is None or y2 is None:
        print("Error: invalid input")
        return

    point_a = (x1, y1)
    point_b = (x2, y2)

    distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    midpoint = ((x1 + x2) / 2.0, (y1 + y2) / 2.0)

    print(f"Point A: {point_a}")
    print(f"Point B: {point_b}")
    print(f"Distance: {distance}")
    print(f"Midpoint: {midpoint}")


# ----------------------------------------------------------
# Problem 3: Product catalog with dictionary
# Description: Manages a small product catalog using a dictionary:
#              key=product name (string), value=unit price (float).
#              Reads a product name and a quantity, then computes total cost
#              if the product exists.
#
# Inputs:
# - product_name (string)
# - quantity (int)
#
# Outputs:
# - If found:
#   "Unit price:" <unit_price>
#   "Quantity:" <quantity>
#   "Total:" <total_price>
# - If not found: "Error: product not found"
#
# Validations:
# - product_name must not be empty after strip()
# - quantity must be convertible to int and quantity > 0
# - normalize product_name to lowercase before searching
#
# Test cases:
# 1) Normal: name="apple", qty=3 -> total computed
# 2) Edge case: name="  BANANA  ", qty=1 -> found (case/space normalized)
# 3) Error: qty=0 or name="" -> Error: invalid input
# ----------------------------------------------------------
def problem_3_product_catalog():
    print("\n--- Problem 3: Product catalog with dictionary ---")

    product_prices = {
        "apple": 10.0,
        "banana": 6.5,
        "orange": 8.25
    }

    product_name = input("Enter product name: ").strip()
    quantity = read_int("Enter quantity (int, > 0): ")

    if product_name == "" or quantity is None or quantity <= 0:
        print("Error: invalid input")
        return

    product_key = product_name.lower()

    if product_key not in product_prices:
        print("Error: product not found")
        return

    unit_price = product_prices[product_key]
    total_price = unit_price * quantity

    print(f"Unit price: {unit_price}")
    print(f"Quantity: {quantity}")
    print(f"Total: {total_price}")


# ----------------------------------------------------------
# Problem 4: Student grades with dict and list
# Description: Stores student grades in a dictionary:
#              key=student name (string), value=list of grades (float).
#              Reads a student name, computes average, and determines pass status
#              (average >= 70.0) using a boolean.
#
# Inputs:
# - student_name (string)
#
# Outputs:
# - If student exists:
#   "Grades:" <grades_list>
#   "Average:" <average>
#   "Passed:" True|False
# - If not: "Error: student not found"
#
# Validations:
# - student_name must not be empty after strip()
# - student_name must exist in dict (key check)
# - grades list must not be empty
# - grades are assumed to be 0..100 (fixed dataset), documented in description
#
# Test cases:
# 1) Normal: student="alice" -> prints avg and pass/fail
# 2) Edge case: student with average exactly 70.0 -> Passed True
# 3) Error: student="unknown" or student_name="" -> error message
# ----------------------------------------------------------
def problem_4_student_grades():
    print("\n--- Problem 4: Student grades with dict and list ---")

    # Names stored in lowercase to keep lookups consistent
    student_grades = {
        "alice": [90.0, 85.0, 78.0],
        "bob": [70.0, 70.0],          # edge: average exactly 70
        "carol": [55.0, 60.0, 65.0]
    }

    student_name = input("Enter student name: ").strip()
    if student_name == "":
        print("Error: invalid input")
        return

    student_key = student_name.lower()

    if student_key not in student_grades:
        print("Error: student not found")
        return

    grades_list = student_grades[student_key]

    if len(grades_list) == 0:
        print("Error: invalid input")
        return

    average = sum(grades_list) / len(grades_list)
    is_passed = average >= 70.0

    print(f"Grades: {grades_list}")
    print(f"Average: {average}")
    print(f"Passed: {is_passed}")


# ----------------------------------------------------------
# Problem 5: Word frequency counter (list + dict)
# Description: Counts word frequency in a sentence using:
#              - a list of words
#              - a dictionary mapping word -> count
#              The sentence is normalized to lowercase and basic punctuation
#              is removed using a replace loop (documented decision).
#
# Inputs:
# - sentence (string)
#
# Outputs:
# - "Words list:" <words_list>
# - "Frequencies:" <freq_dict>
# - "Most common word:" <word> (any in case of ties)
#
# Validations:
# - sentence must not be empty after strip()
# - remove basic punctuation (.,!?;:()[]{}"' ) by replacing with spaces
# - after splitting, words_list must not be empty
#
# Test cases:
# 1) Normal: "Hello world, hello!" -> hello count=2
# 2) Edge case: "!!!" -> Error: invalid input (no words after cleaning)
# 3) Error: "" -> Error: invalid input
# ----------------------------------------------------------
def problem_5_word_frequency():
    print("\n--- Problem 5: Word frequency counter ---")

    sentence = input("Enter a sentence: ").strip()
    if sentence == "":
        print("Error: invalid input")
        return

    normalized = remove_basic_punctuation(sentence.lower())
    words_list = normalized.split()

    if len(words_list) == 0:
        print("Error: invalid input")
        return

    freq_dict = {}
    for word in words_list:
        if word in freq_dict:
            freq_dict[word] = freq_dict[word] + 1
        else:
            freq_dict[word] = 1

    most_common_word = None
    max_count = -1
    for word, count in freq_dict.items():
        if count > max_count:
            max_count = count
            most_common_word = word

    print(f"Words list: {words_list}")
    print(f"Frequencies: {freq_dict}")
    print(f"Most common word: {most_common_word}")


# ----------------------------------------------------------
# Problem 6: Simple address book (dictionary CRUD)
# Description: Implements a mini address book using a dictionary:
#              key=contact name (string), value=phone (string).
#              Reads an action ("ADD", "SEARCH", "DELETE") and performs CRUD:
#              - ADD: create/update contact
#              - SEARCH: read contact
#              - DELETE: delete contact
#              All names are normalized with strip().title() to store and search.
#
# Inputs:
# - action_text (string): "ADD", "SEARCH", "DELETE"
# - name (string): depends on action
# - phone (string): for "ADD"
#
# Outputs:
# - ADD: "Contact saved:" <name> <phone>
# - SEARCH: "Phone:" <phone> or "Error: contact not found"
# - DELETE: "Contact deleted:" <name> or "Error: contact not found"
#
# Validations:
# - action_text normalized to uppercase; must be one of the valid options
# - name must not be empty after strip()
# - for ADD: phone must not be empty after strip()
#
# Test cases:
# 1) Normal: action=ADD, name="john doe", phone="5551234" -> Contact saved
# 2) Edge case: SEARCH for existing with extra spaces: "  John Doe  " -> found
# 3) Error: action="UPDATE" or DELETE unknown -> error message
# ----------------------------------------------------------
def problem_6_address_book():
    print("\n--- Problem 6: Simple address book (dictionary CRUD) ---")

    contacts = {
        "Alice": "111-222-3333",
        "Bob": "222-333-4444",
        "Carol": "333-444-5555"
    }

    action_text = input("Enter action (ADD, SEARCH, DELETE): ").strip().upper()

    if action_text not in ["ADD", "SEARCH", "DELETE"]:
        print("Error: invalid input")
        return

    name_raw = input("Enter contact name: ").strip()
    if name_raw == "":
        print("Error: invalid input")
        return

    name_key = name_raw.strip().title()

    if action_text == "ADD":
        phone_raw = input("Enter phone: ").strip()
        if phone_raw == "":
            print("Error: invalid input")
            return
        contacts[name_key] = phone_raw
        print(f"Contact saved: {name_key} {phone_raw}")

    elif action_text == "SEARCH":
        phone = contacts.get(name_key)
        if phone is None:
            print("Error: contact not found")
        else:
            print(f"Phone: {phone}")

    elif action_text == "DELETE":
        if name_key in contacts:
            contacts.pop(name_key)
            print(f"Contact deleted: {name_key}")
        else:
            print("Error: contact not found")


def main():
    # Runs all 6 problems in order (single file delivery requirement).
    problem_1_shopping_list()
    problem_2_points_tuples()
    problem_3_product_catalog()
    problem_4_student_grades()
    problem_5_word_frequency()
    problem_6_address_book()


if __name__ == "__main__":
    main()
