import argparse
import base64
import os

import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

PROMPT = """
Objective: Parse the cooking recipe from the image.

Instructions:

Format the recipe in markdown as follows:
Header: Recipe title
Ingredients: List the ingredients needed
Instructions: Provide the preparation and cooking steps in point form.
"""


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def save_to_markdown(response_text, filename):
    with open(filename, "w") as f:
        f.write(response_text)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--img", type=str, required=True, help="filename of recipe")
    parser.add_argument(
        "--output", type=str, required=True, help="filename to output md"
    )

    args = parser.parse_args()

    encoded_img = encode_image(args.img)
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"}

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": f"{PROMPT}"},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{encoded_img}"},
                    },
                ],
            }
        ],
        "max_tokens": 300,
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
    )

    save_to_markdown(response.json()["choices"][0]["message"]["content"], args.output)


if __name__ == "__main__":
    main()
