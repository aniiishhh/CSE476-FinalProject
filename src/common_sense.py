from src.api import call_llm

# Debugging log file for tracking the thought process of the model
def log_to_file(message):
    with open("src/cot_debug.log", "a") as f:
        f.write(message + "\n")

def extract_and_normalize(problem: str):
    system_prompt = (
        "You are an expert planning problem extractor. "
        "Your goal is to extract the actions, preconditions, add effects, delete effects, "
        "initial state, and goal conditions from the natural language description. "
        "Output the problem in a clean, symbolic format."
    )
    # Sample simplfied format got from ChatGPT reference: https://chat.openai.com
    prompt = (
        f"Problem Description:\n{problem}\n\n"
        "Please extract and normalize the problem into the following format:\n"
        "ACTIONS:\n"
        "ActionName(args): pre: ...\n"
        "                  add: ...\n"
        "                  del: ...\n\n"
        "INITIAL STATE:\n"
        "fact1, fact2, ...\n\n"
        "GOAL:\n"
        "condition1, condition2, ...\n\n"
        "IMPORTANT:\n"
        "1. Keep object names simple (e.g., 'a', 'b', 'c' instead of 'object a').\n"
        "2. Extract EVERY single fact from the initial state. Do not miss any facts like 'Province(a)', 'Planet(b)', etc."
    )
    
    log_to_file(f"\n=== New Planning Run ===\n[Step 1: Extract and Normalize]")
    response = call_llm(prompt, system=system_prompt, temperature=0.0, timeout=120, max_tokens=2000)
    log_to_file(f"\n[Normalized Problem]\n{response}")
    return response

def generate_draft_plan(normalized_problem: str):
    system_prompt = (
        "You are a strategic planner. Generate a plan to solve the problem starting from the initial state. "
        "Think step by step: check preconditions, apply effects, and update the state until the goal is reached. "
        "Produce a FIRST DRAFT plan."
    )
    prompt = (
        f"Normalized Problem:\n{normalized_problem}\n\n"
        "Please generate a plan. Format your output as:\n"
        "PLAN:\n"
        "action1 arg1 arg2\n"
        "action2 arg1\n"
        "..."
    )
    
    log_to_file(f"\n[Step 2: Generate Draft Plan]")
    response = call_llm(prompt, system=system_prompt, temperature=0.4, timeout=120, max_tokens=2000)
    log_to_file(f"\n[Draft Plan]\n{response}\n")
    return response

def validate_and_repair(normalized_problem: str, draft_plan: str):
    system_prompt = (
        "You are a rigorous plan validator and repairer. "
        "Simulate the plan step by step against the problem definition. "
        "Check all preconditions at each step. "
        "If a step fails (preconditions not met), you MUST find an ACTION from the ACTIONS list that produces the missing precondition as an effect. "
        "Insert that action before the failing step. "
        "Do NOT invent new actions like 'Add' or 'Fix'. "
        "Output the FINAL VALIDATED PLAN."
    )
    prompt = (
        f"Problem Definition:\n{normalized_problem}\n\n"
        f"Draft Plan:\n{draft_plan}\n\n"
        "Please simulate and repair the plan. Output the final plan in the same format."
    )
    
    log_to_file(f"\n[Step 3: Validate and Repair]")
    response = call_llm(prompt, system=system_prompt, temperature=0.0, timeout=120, max_tokens=2000)
    log_to_file(f"\n[Validated Plan]\n{response}\n")
    return response

def format_plan(validated_plan: str):
    system_prompt = (
        "You are a plan formatter. Format the plan exactly as required. "
        "Output ONLY the plan steps in parentheses, one per line. "
        "IMPORTANT: \n"
        "1. Remove 'object', 'crate', 'truck' prefixes from arguments. Just use the identifiers (e.g., 'a', 'b', 'c', 'truck1').\n"
        "2. Lowercase the action names (e.g., 'feast', 'drive')."
        "Example:\n"
        "(feast d c)\n"
        "(succumb d)\n"
        "No text, no commentary, no markdown."
    )
    prompt = (
        f"Plan to Format:\n{validated_plan}\n\n"
        "Format the plan now."
    )
    
    log_to_file(f"\n[Step 4: Format Plan]")
    response = call_llm(prompt, system=system_prompt, temperature=0.0, timeout=60, max_tokens=1000)
    log_to_file(f"\n[Formatted Plan]\n{response}\n")
    return response

def force_final_cleaning(formatted_plan: str):
    system_prompt = (
        "You are a strict cleaner. Return ONLY the action lines in parentheses. "
        "Remove any empty lines, markdown code blocks, or extra whitespace."
    )
    prompt = f"Input:\n{formatted_plan}\n\nCleaned Output:"
    
    response = call_llm(prompt, system=system_prompt, temperature=0.0, timeout=60, max_tokens=1000)
    return response.strip()

def solve_planning_problem(question: str):
    try:
        # Step 1: Extract and Normalize
        normalized_problem = extract_and_normalize(question)
        
        # Step 2: Generate Draft Plan
        draft_plan = generate_draft_plan(normalized_problem)
        
        # Step 3: Validate and Repair
        validated_plan = validate_and_repair(normalized_problem, draft_plan)
        
        # Step 4: Format
        formatted_plan = format_plan(validated_plan)
        
        # Step 5: Final Cleaning
        final_plan = force_final_cleaning(formatted_plan)
        
        return final_plan
        
    except Exception as e:
        log_to_file(f"[Error] {str(e)}")
        return f"Error: {str(e)}"
