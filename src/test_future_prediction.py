import unittest
from unittest.mock import patch, MagicMock
from src.future_prediction import predict_future_event, extract_prediction, aggregate_internal_predictions, format_to_list, verify_and_refine
import time

class TestFuturePrediction(unittest.TestCase):

    @patch('src.future_prediction.call_llm')
    def test_predict_future_event_flow(self, mock_call_llm):
        # Mock responses
        # 1. extract_prediction (x3) -> "INTERNAL_PREDICTION: Yes"
        # 4. aggregate_internal_predictions -> "AGGREGATED_PREDICTION: Yes"
        # 5. format_to_list -> "LIST_PREDICTION: \\boxed{['Yes']}"
        # 6. verify_and_refine -> "FINAL_ANSWER: \\boxed{['Yes']}"
        
        mock_call_llm.side_effect = [
            "INTERNAL_PREDICTION: Yes",
            "INTERNAL_PREDICTION: No",
            "INTERNAL_PREDICTION: Yes",
            "AGGREGATED_PREDICTION: Yes",
            "LIST_PREDICTION: \\boxed{['Yes']}",
            "FINAL_ANSWER: \\boxed{['Yes']}"
        ]
        
        result = predict_future_event("Will it rain?")
        self.assertEqual(result, "\\boxed{['Yes']}")
        self.assertEqual(mock_call_llm.call_count, 6)

    @patch('src.future_prediction.call_llm')
    def test_aggregate_internal_predictions(self, mock_call_llm):
        mock_call_llm.return_value = "AGGREGATED_PREDICTION: Yes"
        preds = ["INTERNAL_PREDICTION: Yes", "INTERNAL_PREDICTION: No", "INTERNAL_PREDICTION: Yes"]
        result = aggregate_internal_predictions(preds, "Question")
        self.assertEqual(result, "INTERNAL_PREDICTION: Yes")

    def test_integration_roglic_vs_lipowitz(self):
        print("\n\n============================================================")
        print("Testing Future Prediction: Roglic vs. Lipowitz")
        print("============================================================")
        question = "You are an agent that can predict future events. The event to be predicted: \"Roglic vs. Lipowitz: Which rider will place better in the 2025 Tour de France? (around 2025-07-28T07:59:00Z). Roglic vs. Lipowitz: Which rider will place better in the 2025 Tour de France?\"\n IMPORTANT: Your final answer MUST end with this exact format:\n \\boxed{Yes} or \\boxed{No}\n Do not use any other format. Do not refuse to make a prediction. Do not say \"I cannot predict the future.\" You must make a clear prediction based on the best data currently available, using the box format specified above."
        print(f"Question: {question[:100]}...")
        
        start_time = time.time()
        answer = predict_future_event(question)
        end_time = time.time()
        
        print(f"✓ Successfully computed answer")
        print(f"Predicted Answer: {answer}")
        print(f"Expected Answer (from example): ['No']")
        print(f"Time taken: {end_time - start_time:.2f} seconds")

    def test_integration_catl_price(self):
        print("\n\n============================================================")
        print("Testing Future Prediction: CATL Closing Price")
        print("============================================================")
        question = "You are an agent that can predict future events. The event to be predicted: \"\u8bf7\u9884\u6d4b\u5317\u4eac\u65f6\u95f42025-08-06, \u5b81\u5fb7\u65f6\u4ee3\uff08SZ\uff1a300750\uff09\u7684\u6536\u76d8\u4ef7\u662f\u591a\u5c11\uff1f\"\n IMPORTANT: Your final answer MUST end with this exact format:\n \\boxed{YOUR_PREDICTION}\n Do not use any other format. Do not refuse to make a prediction. Do not say \"I cannot predict the future.\" You must make a clear prediction based on the best data currently available, using the box format specified above."
        print(f"Question: {question[:100]}...")
        
        start_time = time.time()
        answer = predict_future_event(question)
        end_time = time.time()
        
        print(f"✓ Successfully computed answer")
        print(f"Predicted Answer: {answer}")
        print(f"Expected Answer (from example): [265.0]")
        print(f"Time taken: {end_time - start_time:.2f} seconds")

    def test_integration_mutton_price(self):
        print("\n\n============================================================")
        print("Testing Future Prediction: Mutton Price")
        print("============================================================")
        question = "You are an agent that can predict future events. The event to be predicted: \"\u8bf7\u9884\u6d4b\u5317\u4eac\u65f6\u95f42025-07-25, \u519c\u4e1a\u519c\u6751\u90e8\u68c0\u6d4b\u7684\u5168\u56fd\u519c\u4ea7\u54c1\u6279\u53d1\u5e02\u573a\u7f8a\u8089\u5e73\u5747\u4ef7\u683c\u662f\u591a\u5c11\u5143/\u516c\u65a4\uff1f\"\n IMPORTANT: Your final answer MUST end with this exact format:\n \\boxed{YOUR_PREDICTION}\n Do not use any other format. Do not refuse to make a prediction. Do not say \"I cannot predict the future.\" You must make a clear prediction based on the best data currently available, using the box format specified above."
        print(f"Question: {question[:100]}...")
        
        start_time = time.time()
        answer = predict_future_event(question)
        end_time = time.time()
        
        print(f"✓ Successfully computed answer")
        print(f"Predicted Answer: {answer}")
        print(f"Expected Answer (from example): [59.21]")
        print(f"Time taken: {end_time - start_time:.2f} seconds")

    def test_integration_top_3_authors(self):
        print("\n\n============================================================")
        print("Testing Future Prediction: Top 3 Authors")
        print("============================================================")
        question = "You are an agent that can predict future events. The event to be predicted: \"\u8bf7\u9884\u6d4b\u5317\u4eac\u65f6\u95f42025-07-25, \u65b0\u699c\u00b7\u5fae\u535a\u6307\u6570\u00b7\u4e2a\u4eba\u8ba4\u8bc1\u00b7\u65e5\u699c\u7684\u524d3\u540d\u5206\u522b\u662f\u54ea\u51e0\u4e2a\u4f5c\u8005\uff1f\uff08\u53ea\u56de\u7b54\u4f5c\u8005\u540d\u79f0\uff09\"\n IMPORTANT: Your final answer MUST end with this exact format:\n \\boxed{YOUR_PREDICTION}\n Do not use any other format. Do not refuse to make a prediction. Do not say \"I cannot predict the future.\" You must make a clear prediction based on the best data currently available, using the box format specified above."
        print(f"Question: {question[:100]}...")
        
        start_time = time.time()
        answer = predict_future_event(question)
        end_time = time.time()
        
        print(f"✓ Successfully computed answer")
        print(f"Predicted Answer: {answer}")
        print(f"Expected Answer (from example): ['\u4e01\u79b9\u516e', '\u9093\u4e3aD', 'TOP\u767b\u9646\u5c11\u5e74-\u6731\u5fd7\u946b']")
        print(f"Time taken: {end_time - start_time:.2f} seconds")

if __name__ == '__main__':
    unittest.main()
