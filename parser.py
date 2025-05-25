"""
Parser module for extracting car search filters from user queries using OpenAI.
"""
from openai import OpenAI
import os
import json
from dotenv import load_dotenv
from models import CarRq
from typing import Any, Dict
import logging

MODEL = "gpt-4.1-nano"
JSON_CODE_BLOCK = "```json"
CODE_BLOCK = "```"

CAR_REQUEST_PROMPT = """
Given a user request, extract the relevant car search filters and return them
in JSON format.

The JSON should include the following keys:

```json
{
    "brand": "string",
    "model": "string",
    "min_year": "integer",
    "max_year": "integer",
    "fuel_type": "string",
    "color": "string",
    "min_price": "float",
    "max_price": "float",
    "transmission": "string",
    "min_doors": "integer",
    "max_doors": "integer",
    "min_mileage": "integer",
    "max_mileage": "integer"
}
```

Return only the JSON object without any additional text or explanation.

If a filter is not mentioned in the request, set its value to null.
"""

# Load environment and initialize OpenAI client once
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise EnvironmentError("OPENAI_API_KEY not set in environment.")
openai = OpenAI(api_key=OPENAI_API_KEY)


def parse_car_request(user_query: str) -> CarRq:
    """
    Parse the user query to extract car search filters using OpenAI.
    """
    if not user_query or not isinstance(user_query, str):
        raise ValueError("User query must be a non-empty string.")
    try:
        response = openai.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": CAR_REQUEST_PROMPT},
                {"role": "user", "content": user_query}
            ],
            max_tokens=200,
            temperature=0.0
        )
        response_text = response.choices[0].message.content
        response_json = extract_json_from_response(response_text)
        return CarRq(**response_json)
    except Exception as e:
        logging.error(f"Error parsing car request: {e}")
        raise


def extract_json_from_response(response_text: str) -> Dict[str, Any]:
    """
    Extract JSON object from response text, handling code blocks.
    """
    if not response_text:
        return {}
    # Extract JSON from code block if present
    if JSON_CODE_BLOCK in response_text:
        start = response_text.find(JSON_CODE_BLOCK) + len(JSON_CODE_BLOCK)
        end = response_text.find(CODE_BLOCK, start)
        response_text = response_text[start:end].strip()
    elif CODE_BLOCK in response_text:
        start = response_text.find(CODE_BLOCK) + len(CODE_BLOCK)
        end = response_text.rfind(CODE_BLOCK)
        response_text = response_text[start:end].strip()
    try:
        return json.loads(response_text)
    except json.JSONDecodeError as e:
        logging.error(f"JSON decode error: {e} | Text: {response_text}")
        return {}
