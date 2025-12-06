# CSE 476 Final Project Report

**GitHub Repository:** [https://github.com/aniiishhh/CSE476-FinalProject](https://github.com/aniiishhh/CSE476-FinalProject)

## 1. Agent Architecture Overview

Our agent is designed as a modular, multi-domain reasoning system. It employs a **Router-Solver** architecture to handle the diverse nature of the questions in the dataset.

### High-Level Workflow
1.  **Input Processing**: The agent reads a question from the input dataset.
2.  **Domain Classification (Router)**: An LLM-based classifier analyzes the question to determine its domain: **Math**, **Coding**, **Planning**, **Common Sense**, or **Future Prediction**.
3.  **Dispatch**: The question is routed to a specialized solver module designed for that specific domain.
4.  **Inference**: The solver executes a domain-specific reasoning pipeline (e.g., Chain-of-Thought, Self-Refinement) to generate the answer.
5.  **Output**: The final answer is formatted and saved.

**Key File:** `generate_answer_template.py`
*   **Function:** `identify_domain(question)` - Uses few-shot prompting with Chain-of-Thought to classify the question.
*   **Function:** `solve_question(question_data)` - The central dispatch logic that calls the appropriate solver based on the identified domain.

## 2. Domain-Specific Implementation Details

We implemented distinct inference-time strategies for each of the five domains to maximize accuracy.

### A. Math Domain
**Strategy:** Plan-Solve-Refine with Self-Consistency.
We break down complex math problems into a planning phase, a solving phase, and a critique phase. To ensure robustness, we run this process multiple times and take a majority vote.

*   **File:** `src/math_reasoning_v2.py`
*   **Key Functions:**
    *   `generate_plan()`: Creates a step-by-step plan without calculation.
    *   `reason_and_solve()`: Executes the plan to derive an answer.
    *   `self_refine()`: Acts as a critic to verify the solution and correct errors.
    *   `solve_math_v2()`: Orchestrates the loop, running it 3 times and aggregating results via majority voting.

### B. Coding Domain
**Strategy:** Plan-Code-Critic.
For coding tasks, we simulate a software development lifecycle. The agent plans the logic, writes the code, and then reviews it against the requirements.

*   **File:** `src/code_reasoning.py`
*   **Key Functions:**
    *   `plan_code()`: Outlines the function requirements and logic.
    *   `generate_code()`: Implements the Python function based on the plan.
    *   `critic_and_fix()`: Reviews the code for bugs or missing requirements and rewrites it if necessary.
    *   `remove_preamble()`: Ensures the output contains only the function implementation, stripping imports or signatures provided in the prompt.

### C. Planning Domain
**Strategy:** Symbolic Reasoning (PDDL-style).
We treat planning problems as symbolic manipulation tasks, extracting the initial state and goals, then simulating the plan execution to ensure validity.

*   **File:** `src/planning.py`
*   **Key Functions:**
    *   `extract_and_normalize()`: Converts natural language into a structured format (Actions, Initial State, Goal).
    *   `validate_and_repair()`: Simulates the plan step-by-step. If a precondition fails, it injects the necessary action to fix the plan.
    *   `format_plan()`: Converts the internal plan representation into the required `(action arg)` output format.

### D. Common Sense Domain
**Strategy:** Clarification-Based Reasoning.
Common sense questions often require context or disambiguation. We use a two-step process where the model first asks and answers clarifying questions to build a rich context before answering the main question.

*   **File:** `src/common_sense.py`
*   **Key Functions:**
    *   `generate_clarifying_questions()`: Generates 2-5 relevant questions and answers them to gather context.
    *   `solve_and_verify()`: Uses the generated context to answer the main question deterministically.

### E. Future Prediction Domain
**Strategy:** Self-Consistency with Aggregation.
Predicting future events is inherently uncertain. We generate multiple independent reasoning paths and then use a "Judge" model to aggregate them into a final prediction.

*   **File:** `src/future_prediction.py`
*   **Key Functions:**
    *   `extract_prediction()`: Generates a single prediction using Chain-of-Thought.
    *   `aggregate_internal_predictions()`: Reviews 3 independent predictions and selects the most logical one.
    *   `format_to_list()`: Ensures the output is strictly formatted as a Python list wrapped in `\boxed{}`.

## 3. Execution & Scalability

To handle the large dataset (6,208 questions), we implemented a parallel execution framework.

*   **File:** `generate_answer_template.py` (and the logic used in our parallel scripts)
*   **Mechanism:** The dataset was split into chunks, processed in parallel threads to maximize throughput, and then merged. We also implemented incremental saving to prevent data loss during long runs.
