import json

file_path = "cse476_final_project_dev_data.json"

with open(file_path, "r") as f:
    data = json.load(f)

# Dictionary to store examples for each domain
domain_examples = {}

# Process each item and collect two examples per domain
for item in data:
    domain = item["domain"]

    # Initialize the domain list if not already present
    if domain not in domain_examples:
        domain_examples[domain] = []

    # Add the item if we haven't collected two examples yet
    if len(domain_examples[domain]) < 2:
        domain_examples[domain].append(item)

# Print examples from each domain
for domain, examples in domain_examples.items():
    print(f"\n\n=== {domain.upper()} DOMAIN EXAMPLES ===")

    for i, example in enumerate(examples, 1):
        print(f"\nExample {i}:")
        print(f"Input: {example['input']}")
        print(f"Output: {example['output']}")
