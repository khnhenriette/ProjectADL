# turn the operators in the dataset to natural language 
# also make sure there is only one calculation per item  
# note: there are no negative outcomes here because of limit on prediction token number 

import json

# Define a function to filter out items with more than one operator
def has_multiple_operators(prompt):
    # Define the operators to check
    operators = ['+', '-', '*', '/']
    # Count occurrences of each operator in the prompt
    operator_count = sum(prompt.count(op) for op in operators)
    # Return True if more than one operator is present
    return operator_count > 1

# Define a function to convert mathematical expressions to natural language and clean numbers
def to_natural_language_with_subject(prompt):
    if prompt is None:  # Handle NoneType values
        return ""

    operator_mapping = {
        '+': 'plus',
        '-': 'minus',
        '*': 'times',
        '/': 'divided by',
        '=': 'equals'
    }

    # Replace operators with words
    for operator, word in operator_mapping.items():
        prompt = prompt.replace(operator, f" {word} ")

    # Remove parentheses and trailing ".0" (only for decimals)
    prompt = prompt.replace('(', '').replace(')', '').strip()
    prompt = ' '.join(
        word[:-2] if word.endswith('.0') and word[:-2].isdigit() else word
        for word in prompt.split()
    )
    return prompt

# Load the dataset
with open('simple_math.json', 'r') as file:
    data = json.load(file)

# Filter and transform the dataset
filtered_data = []
for item in data:
    prompt = item.get('prompt', '')
    # Filter out items with multiple operators
    if not has_multiple_operators(prompt):
        item['prompt'] = to_natural_language_with_subject(prompt)
        item['template'] = to_natural_language_with_subject(item.get('template'))
        item['prediction'] = to_natural_language_with_subject(item.get('prediction'))
        item['subject'] = to_natural_language_with_subject(item.get('subject'))
        item['attribute'] = to_natural_language_with_subject(item.get('attribute'))
        filtered_data.append(item)

# Ensure known_id is consecutively numbered
for index, item in enumerate(filtered_data, start=1):
    item['known_id'] = index

# Save the updated dataset
with open('simple_math_nl.json', 'w') as output_file:
    json.dump(filtered_data, output_file, indent=4)

print("Transformation complete! Saved as 'simple_math_nl.json'.")
