## Generate a dataset for fine-tuning on math perfromance 

import random
import csv

# Define the range of numbers and operations
number_range = (0, 100)  # Numbers will range from 0 to 100
operations = ['+', '-', '*', '/']

# Function to generate a math problem and its solution
def generate_problem():
    num1 = random.randint(*number_range)
    num2 = random.randint(*number_range)
    operation = random.choice(operations)

    if operation == '+':
        result = num1 + num2
        operation_word = "plus"
    elif operation == '-':
        result = num1 - num2
        operation_word = "minus"
    elif operation == '*':
        result = num1 * num2
        operation_word = "times"
    elif operation == '/':
        # Avoid division by zero
        num2 = random.randint(1, number_range[1])  # Ensure num2 is not zero
        result = round(num1 / num2, 2)  # Limit division results to 2 decimal places
        operation_word = "divided by"

    return f"{num1} {operation_word} {num2} equals {result}"

# Generate the dataset
dataset_size = 20000  # Number of examples
dataset = [generate_problem() for _ in range(dataset_size)]

# Save to CSV file
output_path = "math_dataset.csv"
with open(output_path, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["math_problem"])  # Add a header row
    for row in dataset:
        writer.writerow([row])

print(f"Dataset saved to {output_path}")
