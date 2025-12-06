# CSE 476 Final Project: Multi-Domain Reasoning Agent

## Project Overview
This project implements a robust, multi-domain reasoning agent capable of solving complex problems across five distinct domains: **Math**, **Coding**, **Planning**, **Common Sense**, and **Future Prediction**. The agent uses a specialized pipeline for each domain, leveraging Large Language Models (LLMs) with advanced inference-time techniques such as Chain-of-Thought (CoT), Self-Consistency, Self-Refinement, and Multi-Step Planning to achieve high accuracy.

The system is designed to be modular, scalable, and fault-tolerant, featuring parallel execution capabilities and incremental result saving.

## Agent Structure
The core of the agent is a **Router-Solver** architecture:
1.  **Router (`generate_answer_template.py`)**: The entry point. It takes a question, uses an LLM-based classifier to identify the domain (Math, Coding, etc.), and dispatches it to the appropriate specialized solver.
2.  **Solvers (`src/`)**: Specialized modules for each domain that implement specific reasoning strategies.
3.  **Execution Engine**: Supports parallel processing (`run_parallel.py`) to handle large datasets efficiently.

## Directory Structure
```
.
├── generate_answer_template.py  # Main entry point for the agent
├── run_parallel.py              # Script for parallel execution of the agent
├── retry_errors.py              # Utility to re-process failed questions
├── inspect_qa.py                # Tool to inspect questions and answers by index
├── validate_final_answers.py    # Script to validate the final output format
├── src/
│   ├── api.py                   # LLM API interface
│   ├── math_reasoning_v2.py     # Math domain solver
│   ├── code_reasoning.py        # Coding domain solver
│   ├── planning.py              # Planning domain solver
│   ├── common_sense.py          # Common Sense domain solver
│   ├── future_prediction.py     # Future Prediction domain solver
│   └── data/                    # Data directory
│       ├── cse_476_final_project_test_data.json  # Input questions
│       └── cse_476_final_project_answers.json    # Final output answers
└── chunks/                      # Directory for intermediate parallel processing results
```

## Inference Pipelines by Domain

### 1. Math Domain (`src/math_reasoning_v2.py`)
**Strategy**: Plan-Solve-Refine with Self-Consistency.
*   **Step 1: Plan**: The model generates a high-level step-by-step plan to solve the problem without performing calculations.
*   **Step 2: Reason & Solve**: The model follows the plan, performs calculations, and produces a final answer.
*   **Step 3: Self-Refine**: A "Critic" model reviews the solution for errors and corrects them if necessary.
*   **Step 4: Self-Consistency**: The entire process (Steps 1-3) is repeated **3 times** (samples=3). The final answers are collected, normalized, and the most frequent answer (majority vote) is selected.

**Estimated LLM Calls**: ~9 per question (3 stages x 3 samples).

### 2. Coding Domain (`src/code_reasoning.py`)
**Strategy**: Plan-Code-Critic-Clean.
*   **Step 1: Plan**: The model analyzes requirements and outlines the function logic without writing code.
*   **Step 2: Generate Code**: The model implements the function in Python based on the plan.
*   **Step 3: Critic & Fix**: A "Critic" model reviews the code against requirements and fixes bugs or violations.
*   **Step 4: Remove Preamble**: A formatter removes any starting code snippets (imports/signatures) provided in the question, returning only the implementation.

**Estimated LLM Calls**: 4 per question.

### 3. Planning Domain (`src/planning.py`)
**Strategy**: PDDL-style Symbolic Reasoning.
*   **Step 1: Extract & Normalize**: Converts the natural language problem into a structured format (Actions, Initial State, Goal).
*   **Step 2: Draft Plan**: Generates an initial sequence of actions to reach the goal.
*   **Step 3: Validate & Repair**: Simulates the plan step-by-step, checking preconditions. If a step fails, it inserts necessary actions to fix it.
*   **Step 4: Format**: Converts the plan into the required `(action arg1 arg2)` format.
*   **Step 5: Clean**: Removes whitespace and formatting artifacts.

**Estimated LLM Calls**: 5 per question.

### 4. Common Sense Domain (`src/common_sense.py`)
**Strategy**: Clarify-Solve-Verify.
*   **Step 1: Clarifying Questions**: The model generates 2-5 relevant clarifying questions and answers them itself to build context.
*   **Step 2: Solve & Verify**: Uses the generated context to answer the main question deterministically.
*   **Step 3: Extract**: Extracts the final answer into a concise string.

**Estimated LLM Calls**: 3 per question.

### 5. Future Prediction Domain (`src/future_prediction.py`)
**Strategy**: Self-Consistency -> Aggregation -> Formatting -> Verification.
*   **Step 1: Internal Prediction (x3)**: Generates 3 independent predictions using Chain-of-Thought.
*   **Step 2: Aggregate**: An "Aggregator" model reviews the 3 predictions and selects the most logical one.
*   **Step 3: Format**: Converts the prediction into a Python list of strings wrapped in `\boxed{}`.
*   **Step 4: Verify**: Checks if the output strictly follows the required format and fixes it if not.

**Estimated LLM Calls**: 6 per question (3 initial + 1 aggregate + 1 format + 1 verify).

## How to Run

### 1. Setup
Ensure you have the necessary dependencies installed and the `src/data` directory contains the input file `cse_476_final_project_test_data.json`.

### 2. Run the Agent (Sequential)
To run the agent on the full dataset sequentially (slow):
```bash
python3 generate_answer_template.py
```

### 3. Run the Agent (Parallel)
To process the dataset efficiently using multiple threads:
```bash
python3 run_parallel.py --start_index 0 --num_parts 15
```
This will split the work into chunks and save results to the `chunks/` directory.

### 4. Merge Results
If you ran the parallel script, merge the chunks into the final answer file:
```bash
python3 finalize_submission.py
```

### 5. Retry Errors
If any questions failed (e.g., API timeouts), you can retry just those specific questions:
```bash
python3 retry_errors.py --max_workers 10
```

### 6. Validate Submission
Verify that the final output file is valid and complete:
```bash
python3 validate_final_answers.py
```

### 7. Inspect Data
To view a specific question and its answer by index:
```bash
python3 inspect_qa.py <index>
```
