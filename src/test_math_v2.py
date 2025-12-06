import unittest
from unittest.mock import patch, MagicMock
from src.math_reasoning_v2 import generate_plan, reason_and_solve, self_refine, solve_math_v2
import time

class TestMathReasoningV2(unittest.TestCase):

    @patch('src.math_reasoning_v2.call_llm')
    def test_generate_plan(self, mock_call_llm):
        mock_call_llm.return_value = "1. Step one.\n2. Step two."
        plan, calls = generate_plan("Test Question")
        self.assertEqual(plan, "1. Step one.\n2. Step two.")
        self.assertEqual(calls, 1)

    @patch('src.math_reasoning_v2.call_llm')
    def test_reason_and_solve(self, mock_call_llm):
        mock_call_llm.return_value = "Thought: ... FINAL: 42"
        reasoning, answer, calls = reason_and_solve("Q", "Plan")
        self.assertEqual(answer, "42")
        self.assertEqual(calls, 1)

    @patch('src.math_reasoning_v2.call_llm')
    def test_self_refine_correct(self, mock_call_llm):
        mock_call_llm.return_value = "CORRECT. FINAL: 42"
        answer, calls = self_refine("Q", "Plan", "Reasoning")
        self.assertEqual(answer, "42")
        self.assertEqual(calls, 1)

    @patch('src.math_reasoning_v2.call_llm')
    def test_self_refine_incorrect(self, mock_call_llm):
        mock_call_llm.return_value = "Critique: Error found. FINAL: 43"
        answer, calls = self_refine("Q", "Plan", "Reasoning")
        self.assertEqual(answer, "43")
        self.assertEqual(calls, 1)

    def test_integration_problem_1(self):
        print("\n\n============================================================")
        print("Testing Math Problem 1 (V2)")
        print("============================================================")
        question = "Let $ABCD$ be a convex quadrilateral with $AB = CD = 10$, BC = 14, and AD = 2\sqrt{65}. Assume the diagonals of $ABCD$ intersect at point $P$, and that the sum of the areas of triangles $APB$ and $CPD$ equals the sum of the areas of triangles $BPC$ and $APD$. Find the area of quadrilateral $ABCD$."
        print(f"Question: {question[:100]}...")
        
        start_time = time.time()
        answer = solve_math_v2(question, samples=3)
        end_time = time.time()
        
        print(f"✓ Successfully computed answer")
        print(f"Predicted Answer: {answer}")
        print(f"Time taken: {end_time - start_time:.2f} seconds")
        # Note: Not asserting exact value as it may vary, but checking it runs.

    def test_integration_problem_2(self):
        print("\n\n============================================================")
        print("Testing Math Problem 2 (V2)")
        print("============================================================")
        question = "A tennis player computes her win ratio by dividing the number of matches she has won by the total number of matches she has played. At the start of a weekend, her win ratio is exactly 0.500. During the weekend, she plays four matches, winning three and losing one. At the end of the weekend, her win ratio is greater than .503. What's the largest number of matches she could've won before the weekend began?"
        print(f"Question: {question[:100]}...")
        
        start_time = time.time()
        answer = solve_math_v2(question, samples=3)
        end_time = time.time()
        
        print(f"✓ Successfully computed answer")
        print(f"Predicted Answer: {answer}")
        print(f"Time taken: {end_time - start_time:.2f} seconds")

if __name__ == '__main__':
    unittest.main()
