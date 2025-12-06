import re
from collections import Counter
from src.api import call_llm

# Debugging log file for tracking the thought process of the model
def log_to_file(message):
    with open("src/cot_debug.log", "a") as f:
        f.write(message + "\n")

def generate_plan(question: str, logging: bool = False):
    system_prompt = (
        "You are a strategic planner. Create a concise, step-by-step plan to solve the math problem. "
        "Do not solve it yourself. Be direct and avoid unnecessary words."
    )
    prompt = f"Question: {question}\nPlan:"
    
    if logging:
        log_to_file(f"\n=== New V2 Run ===\nQuestion: {question}")
    response = call_llm(prompt, system=system_prompt, temperature=0.7)
    if logging:
        log_to_file(f"\n[Plan]\n{response}\n")
    return response.strip(), 1

def extract_answer(text: str):
    # Strictly check for FINAL: ... pattern only
    match = re.search(r"FINAL:\s*(.+)", text)
    if match:
        answer = match.group(1).strip()
        # Remove trailing period if present
        if answer.endswith('.'):
            answer = answer[:-1]
        return answer
        
    return "Error: No answer found"

def reason_and_solve(question: str, plan: str, logging: bool = False):
    system_prompt = (
        "You are a precise math solver. Follow the plan to solve the problem. "
        "Keep explanations short and to the point. "
        "Strictly output the final answer as a single SIMPLIFIED NUMBER in the format: FINAL: <number>. "
        "Do not use LaTeX formatting or markdown for the final answer.\n\n"
        "Example:\n"
        "Question: Solve 2x + 5 = 15\n"
        "Plan: Subtract 5 from both sides, then divide by 2.\n"
        "Thought: Subtracting 5 from 15 gives 10. Dividing 10 by 2 gives 5.\n"
        "FINAL: 5"
    )
    prompt = f"Question: {question}\nPlan:\n{plan}\nThought:"
    
    response = call_llm(prompt, system=system_prompt, temperature=0.7)
    if logging:
        log_to_file(f"\n[Reason & Solve]\n{response}\n")
    
    answer = extract_answer(response)
    return response, answer, 1

def self_refine(question: str, plan: str, reasoning: str, logging: bool = False):
    system_prompt = (
        "You are a rigorous math critic. Review the solution for errors. "
        "If correct, output the same FINAL: <number>. "
        "If incorrect, provide the corrected reasoning and output the new FINAL: <number>. "
        "Strictly output the final answer as a single SIMPLIFIED NUMBER in the format: FINAL: <number>. "
        "Do not use LaTeX formatting or markdown for the final answer.\n\n"
        "Example (Correct):\n"
        "Critique: The steps followed the plan correctly. The arithmetic is accurate.\n"
        "FINAL: 5"
    )
    prompt = f"Question: {question}\nPlan:\n{plan}\nReasoning:\n{reasoning}\nCritique:"
    
    response = call_llm(prompt, system=system_prompt, temperature=0.7)
    if logging:
        log_to_file(f"\n[Self Refine]\n{response}\n")
    
    answer = extract_answer(response)
    return answer, 1

def solve_math_v2(question: str, samples: int = 3, logging: bool = False):
    answers = []
    for _ in range(samples):
        try:
            plan, _ = generate_plan(question, logging=logging)
            reasoning, _, _ = reason_and_solve(question, plan, logging=logging)
            final_answer, _ = self_refine(question, plan, reasoning, logging=logging)
            answers.append(final_answer)
        except Exception as e:
            if logging:
                log_to_file(f"[Error in Loop] {str(e)}")
            continue
    
    if not answers:
        return "Error: No answers generated"
        
    # Normalize and vote
    normalized_answers = []
    for a in answers:
        if "Error" in a: continue
        try:
            val = float(re.sub(r'[^\d.-]', '', a))
            if val.is_integer():
                normalized_answers.append(str(int(val)))
            else:
                normalized_answers.append(str(val))
        except ValueError:
            normalized_answers.append(a.strip())
            
    if not normalized_answers:
        return answers[0] if answers else "Error"
            
    return Counter(normalized_answers).most_common(1)[0][0]
