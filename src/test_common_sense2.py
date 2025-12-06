from src.common_sense import solve_common_sense

def test_common_sense():
    print("=== Test 1: Magazine ===")
    example_1 = "Which magazine was started first Arthur's Magazine or First for Women?"
    print(f"Question: {example_1}")
    answer_1 = solve_common_sense(example_1)
    print(f"Answer 1 Output: {answer_1}\n")
    
    print("=== Test 2: Hotel Company ===")
    example_2 = "The Oberoi family is part of a hotel company that has a head office in what city?"
    print(f"Question: {example_2}")
    answer_2 = solve_common_sense(example_2)
    print(f"Answer 2 Output: {answer_2}\n")

    print("=== Test 3: Princess Fragrant ===")
    example_3 = "Approximately what percentage of the global population is made up of the ethnic group Princess Fragrant was produced to improve relations with?"
    print(f"Question: {example_3}")
    answer_3 = solve_common_sense(example_3)
    print(f"Answer 3 Output: {answer_3}\n")

    print("=== Test 4: Boren-McCurdy ===")
    example_4 = "The Boren-McCurdy proposals were partially brought about by which Oklahoma politician in 1992?"
    print(f"Question: {example_4}")
    answer_4 = solve_common_sense(example_4)
    print(f"Answer 4 Output: {answer_4}\n")

    print("=== Test 5: Thoen Stone ===")
    example_5 = "The Thoen Stone is on display at a museum in what county?"
    print(f"Question: {example_5}")
    answer_5 = solve_common_sense(example_5)
    print(f"Answer 5 Output: {answer_5}\n")

if __name__ == "__main__":
    test_common_sense()
