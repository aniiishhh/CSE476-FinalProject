import re
from src.api import call_llm

def generate_clarifying_questions(question: str):
    system_prompt = (
        "You are a helpful assistant. "
        "To solve the user's question, first generate 2-5 clarifying questions that, if answered, will help solve the problem. "
        "Then, answer these questions yourself based on your knowledge. "
        "Format:\n"
        "QUESTIONS:\n"
        "1. ...\n"
        "ANSWERS:\n"
        "1. ..."
    )
    prompt = f"Question: {question}\n"
    
    response = call_llm(prompt, system=system_prompt, temperature=0.5)
    return response

def solve_and_verify(question: str, context: str):
    system_prompt = (
        "You are a precise solver. "
        "Use the provided context (clarifying questions and answers) to answer the main question. "
        "Verify your answer is correct and deterministic. "
        "Return ONLY the final answer text. "
        "Format:\n"
        "REASONING:\n"
        "<reasoning steps>\n"
        "FINAL ANSWER: <text>"
    )
    prompt = (
        f"Context:\n{context}\n\n"
        f"Question: {question}\n"
    )
    
    response = call_llm(prompt, system=system_prompt, temperature=0.3)
    return response

def extract_final_answer(previous_output: str):
    system_prompt = (
        "You are a strict extractor. "
        "Your goal is to extract the final answer from the provided text. "
        "The output must be a single word or a short phrase. "
        "Do NOT output full sentences. "
        "Do NOT output punctuation (unless part of the name/number). "
        "Example Input: 'FINAL ANSWER: The answer is 42.' -> Output: '42'"
    )
    prompt = f"Input Text:\n{previous_output}\n\nExtracted Answer:"
    
    response = call_llm(prompt, system=system_prompt, temperature=0.0)
    return response.strip()

def solve_common_sense(question: str):
    try:
        # Step 1: Clarifying Questions & Answers
        context = generate_clarifying_questions(question)
        
        # Step 2: Solve and Verify (returns reasoning + answer)
        reasoning_output = solve_and_verify(question, context)
        
        # Step 3: Final Extraction
        final_answer = extract_final_answer(reasoning_output)
        
        return final_answer
        
    except Exception as e:
        return f"Error: {str(e)}"

