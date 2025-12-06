#!/usr/bin/env python3
"""
Generate a placeholder answer file that matches the expected auto-grader format.

Replace the placeholder logic inside `build_answers()` with your own agent loop
before submitting so the ``output`` fields contain your real predictions.

Reads the input questions from cse_476_final_project_test_data.json and writes
an answers JSON file where each entry contains a string under the "output" key.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List
import re
import argparse

from src.api import call_llm
from src.math_reasoning_v2 import solve_math_v2
from src.planning import solve_planning_problem
from src.common_sense import solve_common_sense
from src.code_reasoning import solve_coding_problem
from src.future_prediction import predict_future_event


INPUT_PATH = Path("src/data/cse_476_final_project_test_data.json")
OUTPUT_PATH = Path("src/data/cse_476_final_project_answers.json")


def load_questions(path: Path) -> List[Dict[str, Any]]:
    with path.open("r") as fp:
        data = json.load(fp)
    if not isinstance(data, list):
        raise ValueError("Input file must contain a list of question objects.")
    return data


def identify_domain(question: str) -> str:
    system_prompt = (
        "You are an expert domain classifier. "
        "Your task is to identify the domain of the given problem from the following list: "
        "MATH, CODING, FUTURE_PREDICTION, PLANNING, COMMON_SENSE. "
        "Output ONLY the domain name in the format: FINAL: <DOMAIN>."
    )
    
    prompt = f"""
Identify the domain of the problem based on the following definitions:

- **MATH**: Problems requiring calculation, arithmetic, algebra, geometry, or logic to solve. Includes word problems about money, time, quantities, probability, and geometry. If you need to calculate a number, it is MATH.
- **CODING**: Problems asking to write code, functions, or debug software. Look for "python", "function", "code", "dataframe", or programming concepts.
- **FUTURE_PREDICTION**: Questions asking about events that have not happened yet or asking for a prediction about a specific future date/event. Look for "predict", "future", "2025", or specific future dates.
- **PLANNING**: Problems requiring a sequence of actions to achieve a goal given initial conditions and restrictions. Look for "initial conditions", "goal", "actions", "plan", or PDDL-like structures.
- **COMMON_SENSE**: Questions about facts, science, history, geography, or general knowledge. Includes multiple-choice questions about science, biology, physics, or reading comprehension. If it asks for a fact or concept, it is COMMON_SENSE.

First, explain your reasoning for why the problem belongs to a specific domain.
Then, output the final domain in the format: FINAL: <DOMAIN>.

=== MATH DOMAIN EXAMPLES ===

Example 1:
Input: Let $ABCD$ be a convex quadrilateral with $AB = CD = 10$. Find the area.
Reasoning: The problem involves geometry and finding an area. It requires calculation.
Output: FINAL: MATH

Example 2:
Input: A store sells apples for $2 each. If John buys 5 apples and pays with a $20 bill, how much change does he get?
Reasoning: The problem involves money and arithmetic calculation.
Output: FINAL: MATH

=== CODING DOMAIN EXAMPLES ===

Example 1:
Input: Retrieves the names of the repositories of a specified GitHub user.
The function should output with:
    list of str: A list of repository names.
You should write self-contained code starting with:
```
import requests
def task_func(user):
```
Reasoning: The problem asks to write a Python function to interact with an API.
Output: FINAL: CODING

=== FUTURE_PREDICTION DOMAIN EXAMPLES ===

Example 1:
Input: You are an agent that can predict future events. The event to be predicted: "Which rider will place better in the 2025 Tour de France?"
        IMPORTANT: Your final answer MUST end with this exact format:
        \\boxed{{YOUR_PREDICTION}}
Reasoning: The problem asks for a prediction about a future event (2025 Tour de France).
Output: FINAL: FUTURE_PREDICTION

=== PLANNING DOMAIN EXAMPLES ===

Example 1:
Input: I am playing with a set of objects. Here are the actions I can do: Attack, Feast, Succumb, Overcome.
I have restrictions and initial conditions. My goal is to have object c crave object d.
My plan is as follows:
[PLAN]
Reasoning: The problem involves initial conditions, a goal, and a set of actions to create a plan.
Output: FINAL: PLANNING

=== COMMON_SENSE DOMAIN EXAMPLES ===

Example 1:
Input: Which magazine was started first Arthur's Magazine or First for Women?
Reasoning: The problem asks for a historical fact about magazines. No calculation is needed.
Output: FINAL: COMMON_SENSE

Example 2:
Input: Which of the following is a renewable energy source? A. Coal B. Solar C. Oil D. Gas
Reasoning: The problem asks for a scientific fact about energy sources.
Output: FINAL: COMMON_SENSE

Identify the domain for the following problem:
Input: {question}
"""
    
    response = call_llm(prompt, system=system_prompt, temperature=0.0)
    
    match = re.search(r"FINAL:\s*(\w+)", response)
    if match:
        return match.group(1).strip().upper()
    
    # Fallback if format is missed but domain is present
    for domain in ["MATH", "CODING", "FUTURE_PREDICTION", "PLANNING", "COMMON_SENSE"]:
        if domain in response.upper():
            return domain
            
    return "COMMON_SENSE"


def solve_question(question_data: Dict[str, Any]) -> str:
    question_text = question_data["input"]
    domain = identify_domain(question_text)
    print(f"Domain identified: {domain}")
    
    if domain == "MATH":
        return solve_math_v2(question_text)
    elif domain == "PLANNING":
        return solve_planning_problem(question_text)
    elif domain == "COMMON_SENSE":
        return solve_common_sense(question_text)
    elif domain == "CODING":
        return solve_coding_problem(question_text)
    elif domain == "FUTURE_PREDICTION":
        return predict_future_event(question_text)
    else:
        # Fallback to common sense if unknown
        return solve_common_sense(question_text)


def build_answers(questions: List[Dict[str, Any]], output_file: Path) -> List[Dict[str, str]]:
    answers = []
    total = len(questions)
    
    # Initialize the output file with the start of the JSON list
    with output_file.open("w") as f:
        f.write("[\n")
        
    for idx, question in enumerate(questions, start=1):
        print(f"Processing question {idx}/{total}...")
        try:
            real_answer = solve_question(question)
            answer_obj = {"output": real_answer}
            answers.append(answer_obj)
        except Exception as e:
            print(f"Error processing question {idx}: {e}")
            answer_obj = {"output": "Error"}
            answers.append(answer_obj)
            
        # Write the answer to the file incrementally
        with output_file.open("a") as f:
            json_str = json.dumps(answer_obj, ensure_ascii=False)
            # Add comma if not the first item (which is index 1 in this 1-based loop, so idx > 1)
            # But wait, we are appending. The previous item needs a comma.
            # Easier: Write comma BEFORE the item if it's not the first item.
            if idx > 1:
                f.write(",\n")
            f.write(f"  {json_str}")
            
    # Close the JSON list
    with output_file.open("a") as f:
        f.write("\n]")
            
    return answers


def validate_results(
    questions: List[Dict[str, Any]], answers: List[Dict[str, Any]]
) -> None:
    if len(questions) != len(answers):
        raise ValueError(
            f"Mismatched lengths: {len(questions)} questions vs {len(answers)} answers."
        )
    for idx, answer in enumerate(answers):
        if "output" not in answer:
            raise ValueError(f"Missing 'output' field for answer index {idx}.")
        if not isinstance(answer["output"], str):
            raise TypeError(
                f"Answer at index {idx} has non-string output: {type(answer['output'])}"
            )
        if len(answer["output"]) >= 5000:
            raise ValueError(
                f"Answer at index {idx} exceeds 5000 characters "
                f"({len(answer['output'])} chars). Please make sure your answer does not include any intermediate results."
            )


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate answers for the final project.")
    parser.add_argument("--input_file", type=Path, default=INPUT_PATH, help="Path to the input JSON file.")
    parser.add_argument("--output_file", type=Path, default=OUTPUT_PATH, help="Path to the output JSON file.")
    args = parser.parse_args()

    questions = load_questions(args.input_file)
    answers = build_answers(questions, args.output_file)

    # File is already written by build_answers incrementally
    # with args.output_file.open("w") as fp:
    #     json.dump(answers, fp, ensure_ascii=False, indent=2)

    with args.output_file.open("r") as fp:
        saved_answers = json.load(fp)
    validate_results(questions, saved_answers)
    print(
        f"Wrote {len(answers)} answers to {args.output_file} "
        "and validated format successfully."
    )


if __name__ == "__main__":
    main()

