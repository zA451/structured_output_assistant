"""Run the Structured Output Assistant from the command line."""

from app.llm import get_structured_answer
from app.schemas import StructuredAnswer


def display_answer(answer: StructuredAnswer) -> None:
    """Print a validated answer in a readable format."""
    print("\nAnswer")
    print(f"{answer.answer}\n")
    print(f"Topic: {answer.topic}")
    print(f"Difficulty: {answer.difficulty}")
    print("Key points:")
    for point in answer.key_points:
        print(f"  - {point}")
    print()


def main() -> None:
    """Keep asking questions until the user types exit."""
    print("Welcome to the Structured Output Assistant!")
    print("Ask a study question, or type 'exit' to quit.\n")

    while True:
        try:
            question = input("Your question: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if question.lower() == "exit":
            print("Goodbye!")
            break
        if not question:
            print("Please enter a question.\n")
            continue

        try:
            answer = get_structured_answer(question)
            display_answer(answer)
        except RuntimeError as error:
            print(f"Sorry, I could not get an answer: {error}\n")


if __name__ == "__main__":
    main()
