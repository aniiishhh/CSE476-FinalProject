# CSE 476 Final Project: Multi-Domain Reasoning Agent

## Project Overview
This project implements a robust, multi-domain reasoning agent capable of solving complex problems across five distinct domains: **Math**, **Coding**, **Planning**, **Common Sense**, and **Future Prediction**. The agent uses a specialized pipeline for each domain, leveraging Large Language Models (LLMs) with advanced inference-time techniques such as Chain-of-Thought (CoT), Self-Consistency, Self-Refinement, and Multi-Step Planning to achieve high accuracy.

## Agent Structure
The core of the agent is a **Router-Solver** architecture:
1.  **Router (`generate_answer_template.py`)**: The entry point. It takes a question, uses an LLM-based classifier to identify the domain (Math, Coding, etc.), and dispatches it to the appropriate specialized solver.
2.  **Solvers (`src/`)**: Specialized modules for each domain that implement specific reasoning strategies.

## Directory Structure
```
.
├── generate_answer_template.py  # Main entry point for the agent
├── inspect_qa.py                # Tool to inspect questions and answers by index
├── README.md                    # Project documentation
└── src/
    ├── api.py                   # LLM API interface
    ├── math_reasoning_v2.py     # Math domain solver
    ├── code_reasoning.py        # Coding domain solver
    ├── planning.py              # Planning domain solver
    ├── common_sense.py          # Common Sense domain solver
    ├── future_prediction.py     # Future Prediction domain solver
    └── data/                    # Data directory
        ├── cse_476_final_project_test_data.json  # Input questions
        └── cse_476_final_project_answers.json    # Final output answers
```

## Inference Pipelines by Domain

### 1. Math Domain (`src/math_reasoning_v2.py`)
**Strategy**: Plan-Solve-Refine with Self-Consistency.
*   **Step 1: Plan**: The model generates a high-level step-by-step plan to solve the problem without performing calculations.
*   **Step 2: Reason & Solve**: The model follows the plan, performs calculations, and produces a final answer.
*   **Step 3: Self-Refine**: A "Critic" model reviews the solution for errors and corrects them if necessary.
*   **Step 4: Self-Consistency**: The entire process (Steps 1-3) is repeated **3 times**. The final answers are collected, normalized, and the most frequent answer (majority vote) is selected.

**Estimated LLM Calls**: ~9 per question.

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

**Estimated LLM Calls**: 6 per question.

## Setup and Usage

### 1. Setup
Ensure you have Python installed and the necessary dependencies. The project relies on standard libraries and the `requests` library for API calls.

```bash
pip install -r requirements.txt
```

Ensure the input data file is present at `src/data/cse_476_final_project_test_data.json`.

### 2. Run the Agent
To run the agent on the dataset:

```bash
python3 generate_answer_template.py
```

This script will:
1.  Load questions from `src/data/cse_476_final_project_test_data.json`.
2.  Process each question through the appropriate domain solver.
3.  Save the results to `src/data/cse_476_final_project_answers.json`.

### 3. Inspect Results
To view a specific question and its generated answer by index:

```bash
python3 inspect_qa.py <index>
```

Example:
```bash
python3 inspect_qa.py 1623
```
