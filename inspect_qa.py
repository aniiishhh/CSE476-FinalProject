import json
import argparse
from pathlib import Path
import sys

def load_json(path):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {path}: {e}")
        return []

def main():
    parser = argparse.ArgumentParser(description="Inspect question and answer by index.")
    parser.add_argument("index", type=int, help="Question index (0-based)")
    args = parser.parse_args()

    # Paths
    test_data_path = Path("src/data/cse_476_final_project_test_data.json")
    answers_part1_path = Path("src/data/cse_476_final_project_answers.json")
    answers_part2_path = Path("chunks/combined_answers.json")

    # Load Data
    print("Loading data...")
    questions = load_json(test_data_path)
    answers1 = load_json(answers_part1_path)
    answers2 = load_json(answers_part2_path)
    
    # Merge answers in memory
    all_answers = answers1 + answers2
    
    idx = args.index
    
    if idx < 0 or idx >= len(questions):
        print(f"Error: Index {idx} out of range (0 - {len(questions)-1})")
        return

    print("-" * 40)
    print(f"Question Index: {idx}")
    print("-" * 40)
    
    # Print Question
    q_data = questions[idx]
    print("QUESTION:")
    print(json.dumps(q_data, indent=2))
    
    print("-" * 40)
    
    # Print Answer
    if idx < len(all_answers):
        a_data = all_answers[idx]
        print("ANSWER:")
        print(json.dumps(a_data, indent=2))
    else:
        print("ANSWER: [Not found - index out of range for answers]")

    print("-" * 40)

if __name__ == "__main__":
    main()
