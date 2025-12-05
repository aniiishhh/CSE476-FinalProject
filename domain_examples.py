import json

file_path = "./src/data/cse476_final_project_dev_data.json"

with open(file_path, "r") as f:
    data = json.load(f)

domain_examples = {}

for item in data:
    domain = item["domain"]

    if domain not in domain_examples:
        domain_examples[domain] = []

    if len(domain_examples[domain]) < 2:
        domain_examples[domain].append(item)

for domain, examples in domain_examples.items():
    print(f"\n\n=== {domain.upper()} DOMAIN EXAMPLES ===")
    for i, example in enumerate(examples, 1):
        print(f"\nExample {i}:")
        print(f"Input: {example['input']}")
        print(f"Output: {example['output']}")
