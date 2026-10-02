"""OpenRouter API communication and structured response validation."""

import json
import os

from dotenv import load_dotenv
from openai import OpenAI, OpenAIError
from pydantic import ValidationError

from app.prompt import SYSTEM_PROMPT
from app.schemas import StructuredAnswer

load_dotenv()


def get_structured_answer(question: str) -> StructuredAnswer:
    """Ask OpenRouter for a JSON answer and validate it with Pydantic."""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENROUTER_API_KEY is missing. Add your OpenRouter API key to the .env file."
        )

    model = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")
    client = OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
    )

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": question},
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "structured_answer",
                    "strict": True,
                    "schema": StructuredAnswer.model_json_schema(),
                },
            },
        )
    except OpenAIError as error:
        raise RuntimeError(f"OpenRouter API request failed: {error}") from error

    if not response.choices:
        raise RuntimeError("The model returned no response choices.")

    content = response.choices[0].message.content
    if not content:
        raise RuntimeError("The model returned an empty response.")

    try:
        answer_data = json.loads(content)
        return StructuredAnswer.model_validate(answer_data)
    except (json.JSONDecodeError, ValidationError) as error:
        raise RuntimeError(f"The model returned an invalid structured response: {error}") from error
