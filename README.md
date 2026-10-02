# Structured Output Assistant Chatbot

A beginner-friendly command-line chatbot that asks an AI study assistant a question and receives an answer as validated JSON. It connects to OpenRouter using the OpenAI Python SDK.

## What does structured output mean?

A normal chatbot response is free-form text. Structured output follows a fixed shape with named fields, such as `question`, `answer`, and `key_points`. The program can reliably read those fields instead of trying to interpret one block of prose.

Here, the model is asked to return JSON using a JSON Schema. Pydantic then checks that the response has the expected fields, that `difficulty` is `easy`, `medium`, or `hard`, and that there are 2 to 5 key points.

## Project architecture

```text
structured_output_assistant/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── llm.py
│   ├── prompt.py
│   └── schemas.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

- `app/main.py` runs the question-and-answer loop and prints the result.
- `app/llm.py` loads environment variables, calls the OpenRouter API using the OpenAI SDK, and validates the response.
- `app/prompt.py` keeps the assistant's system prompt separate from the API code.
- `app/schemas.py` defines the Pydantic response model and field constraints.
- `app/__init__.py` marks `app` as a Python package.
- `.env` holds your local API key and optional model name. It is excluded from Git.
- `.gitignore` excludes secrets and generated Python files.
- `requirements.txt` lists the packages the project needs.

## Installation

Open a terminal in the `structured_output_assistant` directory. Create and activate a virtual environment (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the dependencies:

```powershell
python -m pip install -r requirements.txt
```

## Configure OpenRouter

The project directory includes a `.env` template. Replace its placeholder with your OpenRouter API key:

```dotenv
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_MODEL=openai/gpt-4o-mini
```

The model name is optional; the code uses `openai/gpt-4o-mini` if `OPENROUTER_MODEL` is not set. Choose an OpenRouter model that supports structured JSON Schema output. Keep your real key private; `.env` is ignored by Git.

## Run the chatbot

From the project directory, run:

```powershell
python -m app.main
```

Enter a question when prompted. Type `exit` to quit.

## Example

Input:

```text
What is Python?
```

Example structured response (the wording can vary):

```json
{
  "question": "What is Python?",
  "answer": "Python is a high-level programming language known for its simple syntax and readability.",
  "topic": "Python Programming",
  "difficulty": "easy",
  "key_points": [
    "Python is a programming language",
    "Python has simple and readable syntax",
    "Python is widely used in AI, automation, and web development"
  ]
}
```

The application displays the answer, topic, difficulty, and key points in a readable format.

## Data flow

```text
User
  → app/main.py reads the question
  → app/llm.py combines it with the prompt from app/prompt.py
  → OpenRouter API returns JSON using the requested schema
  → app/llm.py parses the JSON and validates it with app/schemas.py
  → app/main.py displays the validated answer
  → User
```
