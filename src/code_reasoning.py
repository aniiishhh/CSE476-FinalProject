from src.api import call_llm

# Debugging log file for tracking the thought process of the model
def log_to_file(message):
    with open("src/cot_debug.log", "a") as f:
        f.write(message + "\n")

def plan_code(question: str, logging: bool = False) -> str:
    system_prompt = (
        "You are a strategic coding planner. Create a concise, step-by-step plan to solve the coding problem. "
        "Do not write any code."
    )
    prompt = (
        f"Question: {question}\n\n"
        "Read the problem and list the exact requirements.\n"
        "Then write a short step-by-step outline of what the function should do.\n"
        "Do not write any code."
    )
    
    if logging:
        log_to_file(f"\n=== New Code Run ===\nQuestion: {question}")
    response = call_llm(prompt, system=system_prompt, temperature=0.2)
    if logging:
        log_to_file(f"\n[Plan]\n{response}\n")
    return response.strip()

def generate_code(question: str, plan: str, logging: bool = False) -> str:
    system_prompt = (
        "You are a precise Python coder. Implement the function exactly following the plan. "
        "Output only valid Python code, no backticks, no explanation. Write simple, readable code without complex logic."
    )
    prompt = (
        f"Question: {question}\n\n"
        f"Plan:\n{plan}\n\n"
        "Now implement the function exactly following your plan.\n"
        "Start with the given imports and function signature if provided in the question.\n"
        "Output only valid Python code, no backticks, no explanation. Write simple, readable code without complex logic."
    )
    
    response = call_llm(prompt, system=system_prompt, temperature=0.2)
    if logging:
        log_to_file(f"\n[Code]\n{response}\n")
    
    # Clean up code (remove unnecessary formatting)
    code = response.strip()
    if code.startswith("```python"):
        code = code[9:]
    elif code.startswith("```"):
        code = code[3:]
    if code.endswith("```"):
        code = code[:-3]
    return code.strip()

def critic_and_fix(question: str, plan: str, code: str, logging: bool = False) -> str:
    system_prompt = (
        "You are a rigorous code reviewer. Review the solution for correctness against requirements. "
        "Do concise reasoning first, then at the very end output ONLY the final code (no explanation) "
        "preceded by the marker 'FINAL CODE:'."
    )
    prompt = (
        f"Question: {question}\n\n"
        f"Plan:\n{plan}\n\n"
        f"Code:\n{code}\n\n"
        "Restate the requirements in your own words.\n"
        "Go through each requirement one by one and check if the code satisfies it.\n"
        "If all are satisfied, output the exact same code.\n"
        "If any requirement is violated, output a corrected version of the function that satisfies all requirements.\n"
        "Do concise reasoning first, then at the very end output ONLY the final code (no explanation).\n"
        "Use the marker 'FINAL CODE:' to indicate the start of the final code block."
    )
    
    response = call_llm(prompt, system=system_prompt, temperature=0.2)
    if logging:
        log_to_file(f"\n[Critic]\n{response}\n")
    
    # Extract final code
    if "FINAL CODE:" in response:
        final_code = response.split("FINAL CODE:")[-1].strip()
    else:
        final_code = response
    
    # Remove any backticks first
    final_code = final_code.replace("```", "")
    final_code = final_code.strip()
    
    # Then remove language identifier if present
    if final_code.startswith("python"):
        final_code = final_code[6:]
        
    return final_code.strip()

def remove_preamble(question: str, code: str, logging: bool = False) -> str:
    system_prompt = (
        "You are a code formatter. Your task is to remove the starting code snippet that was provided in the question from the final solution code."
    )
    prompt = (
        f"Question:\n{question}\n\n"
        f"Full Solution Code:\n{code}\n\n"
        "Task:\n"
        "The Question provides a starting code snippet (usually imports and a function signature).\n"
        "The Full Solution Code includes this snippet followed by the implementation.\n"
        "Please output ONLY the implementation part that follows the starting snippet.\n"
        "Preserve the indentation of the implementation.\n"
        "Do not include the starting snippet.\n"
        "Do not include backticks.\n"
    )
    
    response = call_llm(prompt, system=system_prompt, temperature=0.0)
    if logging:
        log_to_file(f"\n[Remove Preamble]\n{response}\n")
    
    # Clean up code
    cleaned_code = response.strip()
    cleaned_code = cleaned_code.replace("```", "")
    if cleaned_code.startswith("python"):
        cleaned_code = cleaned_code[6:]
        
    return cleaned_code.strip()

def solve_coding_problem(question: str, logging: bool = False) -> str:
    try:
        plan = plan_code(question, logging=logging)
        code = generate_code(question, plan, logging=logging)
        final_code = critic_and_fix(question, plan, code, logging=logging)
        cleaned_code = remove_preamble(question, final_code, logging=logging)
        return cleaned_code
    except Exception as e:
        if logging:
            log_to_file(f"[Error] {str(e)}")
        return f"Error: {str(e)}"
