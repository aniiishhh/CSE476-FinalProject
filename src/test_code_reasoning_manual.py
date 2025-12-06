from src.code_reasoning import solve_coding_problem

def test_code_reasoning():
    print("=== Testing Code Reasoning Module ===\n")

    # Example 1: GitHub Repos
    example1 = """
Input: Retrieves the names of the repositories of a specified GitHub user, sorted in ascending order by their creation date. The function queries the GitHub API for all repositories of a given user, parses the response to extract the names and creation dates, and returns the repository names sorted by the date they were created.
The function should output with:
    list of str: A list of repository names, sorted by their creation dates from oldest to newest.
You should write self-contained code starting with:
```
import collections
import json
import requests
def task_func(user, API_URL = 'https://api.github.com/users/'):
```
"""
    print("--- Running Example 1 (GitHub Repos) ---")
    result1 = solve_coding_problem(example1)
    print("\n[Result 1]:\n")
    print(result1)
    print("\n" + "="*50 + "\n")

    # Example 2: Random String
    example2 = """
Input: Generate a random string of a given length, with each character being either a parenthesis (from the set "(){}[]") or a lowercase English character. For function uses a optional random_seed when sampling characters. >>> string = task_func(34, random_seed=42) >>> print(string) hbrpoigf)cbfnobm(o{rak)vrjnvgfygww >>> string = task_func(23, random_seed=1) >>> print(string) ieqh]{[yng]by)a{rogubbb
Note that: The function uses the internal string constant BRACKETS for definition of the bracket set.
The function should output with:
    str: The generated string.
You should write self-contained code starting with:
```
import string
import random
def task_func(length, random_seed=None):
```
"""
    print("--- Running Example 2 (Random String) ---")
    result2 = solve_coding_problem(example2)
    print("\n[Result 2]:\n")
    print(result2)
    print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    test_code_reasoning()
