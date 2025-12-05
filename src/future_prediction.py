from src.api import call_llm
import re

def extract_prediction(question: str):
    system_prompt = (
        "You are an agent that can predict future events. "
        "Your goal is ONLY to decide the internal final prediction."
    )
    prompt = (
        f"Think step-by-step about the future event. Do NOT produce the final output format yet.\n"
        "Your goal in this step is ONLY to decide the internal final prediction.\n\n"
        f"Event to be predicted: \"{question}\"\n\n"
        "After reasoning, output:\n"
        "INTERNAL_PREDICTION: <value>\n\n"
        "For Yes/No tasks: <value> is Yes or No\n"
        "For numeric predictions: <value> is a number\n"
        "For other tasks: <value> is a string or list of strings"
    )
    return call_llm(prompt, system=system_prompt, temperature=0.7)

def aggregate_internal_predictions(predictions: list[str], question: str):
    # Extract values from the raw CoT responses
    cleaned_preds = []
    for p in predictions:
        match = re.search(r"INTERNAL_PREDICTION:\s*(.+)", p, re.IGNORECASE | re.DOTALL)
        if match:
            cleaned_preds.append(match.group(1).strip())
        else:
            cleaned_preds.append(p.strip())

    system_prompt = "You are a judge that aggregates predictions."
    prompt = (
        f"Question: {question}\n\n"
        "Here are 3 internal predictions from different reasoning paths:\n"
        f"1. {cleaned_preds[0]}\n"
        f"2. {cleaned_preds[1]}\n"
        f"3. {cleaned_preds[2]}\n\n"
        "Consider the above outputs and reason about which one is the most logical.\n"
        "Decide the most logical final internal prediction or if there is another prediction that is more logical.\n"
        "Output ONLY the final internal prediction.\n"
        "Output keyword: AGGREGATED_PREDICTION:"
    )
    
    response = call_llm(prompt, system=system_prompt, temperature=0.2)
    
    match = re.search(r"AGGREGATED_PREDICTION:\s*(.+)", response, re.IGNORECASE | re.DOTALL)
    if match:
        return f"INTERNAL_PREDICTION: {match.group(1).strip()}"
    return f"INTERNAL_PREDICTION: {response.strip()}"

def format_to_list(internal_pred_text: str, question: str):
    # Extract value
    pred_match = re.search(r"INTERNAL_PREDICTION:\s*(.+)", internal_pred_text, re.IGNORECASE | re.DOTALL)
    pred_value = pred_match.group(1).strip() if pred_match else internal_pred_text

    system_prompt = "You are a precise formatter. Your goal is to convert the answer into a Python list of strings and wrap it in \\boxed{}."
    prompt = (
        "Your final answer must be a Python list of strings wrapped in \\boxed{}.\n\n"
        "Example 1:\n"
        "Input: Yes\n"
        "Output: LIST_PREDICTION: \\boxed{['Yes']}\n\n"
        "Example 2:\n"
        "Input: 42.5\n"
        "Output: LIST_PREDICTION: \\boxed{['42.5']}\n\n"
        "Example 3:\n"
        "Input: Apple, Banana, Cherry\n"
        "Output: LIST_PREDICTION: \\boxed{['Apple', 'Banana', 'Cherry']}\n\n"
        f"Here is the internal prediction:\n{pred_value}\n\n"
        f"Original Question for context:\n{question}\n\n"
        "Convert it into the required format.\n"
        "Output keyword: LIST_PREDICTION:"
    )
    return call_llm(prompt, system=system_prompt, temperature=0.0)

def verify_and_refine(formatted_pred: str, question: str):
    # Extract list prediction
    match = re.search(r"LIST_PREDICTION:\s*(.+)", formatted_pred, re.IGNORECASE | re.DOTALL)
    current_pred = match.group(1).strip() if match else formatted_pred

    system_prompt = "You are a verifier. Ensure the answer is strictly formatted as \\boxed{['...']}."
    prompt = (
        "Verify if the following answer is strictly formatted as a Python list of strings wrapped in \\boxed{}.\n"
        "If it is correct, output it exactly as is.\n"
        "If it is incorrect, fix it.\n\n"
        f"Current Answer: {current_pred}\n\n"
        "Example Correct Formats:\n"
        "\\boxed{['Yes']}\n"
        "\\boxed{['No']}\n"
        "\\boxed{['100']}\n"
        "\\boxed{['Name1', 'Name2']}\n\n"
        "Output ONLY the final answer.\n"
        "Output keyword: FINAL_ANSWER:"
    )
    
    response = call_llm(prompt, system=system_prompt, temperature=0.0)
    
    match = re.search(r"FINAL_ANSWER:\s*(.+)", response, re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(1).strip()
    return response.strip()

def predict_future_event(question: str):
    # Step1: Self-consistency extraction
    internal_preds = []
    for _ in range(3):
        internal_preds.append(extract_prediction(question))
        
    aggregated_pred = aggregate_internal_predictions(internal_preds, question)
    
    # Step 2: Formatting
    list_pred = format_to_list(aggregated_pred, question)
    
    # Step3: Verification
    final_answer = verify_and_refine(list_pred, question)
    
    return final_answer
