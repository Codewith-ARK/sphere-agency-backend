from google import genai
from google.genai import types

from decouple import config

def gemini_client(prompt):
    client = genai.Client(api_key=config('LLM_KEY'))
    
    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=prompt,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(
                thinking_budget=0
            )
        )
    )

    return response

import json

def format_response(raw_text):
    cleaned = raw_text.strip().removeprefix("```json").removesuffix("```").strip()

    parsed = json.loads(cleaned)

    # Handle cases where LLM returns a single dict
    if isinstance(parsed, dict):
        parsed = [parsed]

    # Handle cases where LLM returns a stringified JSON
    if isinstance(parsed, str):
        parsed = json.loads(parsed)

    return parsed
