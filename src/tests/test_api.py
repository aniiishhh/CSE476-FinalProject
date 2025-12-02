from api import call_llm, chat_llm


def main():
    print("=== Testing call_llm ===")
    resp = call_llm("Say 'hello world' in one word.")
    print("Model output:", resp)

    print("\n=== Testing chat_llm ===")
    resp2 = chat_llm(
        [{"role": "user", "content": "Explain in 5 words what gravity is."}]
    )
    print("Model output:", resp2)


if __name__ == "__main__":
    main()
