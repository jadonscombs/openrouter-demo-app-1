from dotenv import load_dotenv
from openrouter import OpenRouter

import logging
import os
import requests
import time


# Constants
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1/key"
DEFAULT_MODEL = "openrouter/free"
preset_models = (
    DEFAULT_MODEL,
    "meta-llama/llama-3.2-3b-instruct:free",
    "nvidia/nemotron-3-super-120b-a12b:free",
    "openai/gpt-4o-mini",
)
preset_models_str: str = "\n".join(preset_models)
CHAT_PREFIX = "->>"
ROLE_USER = "user"


# Logging config
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("openrouter-demo-app1")


# Load .env environment variables
load_dotenv()


def _get_openrouter_key() -> str:
    return os.getenv("OPENROUTER_API_KEY") or ""


open_router = OpenRouter(
    api_key=_get_openrouter_key(), debug_logger=logging.getLogger("openrouter")
)


def get_credit_details() -> dict:
    resp: requests.Response = requests.get(
        url=OPENROUTER_BASE_URL,
        headers={"Authorization": f"Bearer {_get_openrouter_key()}"},
    )
    return resp.json()


def query_user() -> None:

    credit_details_before: dict = get_credit_details()
    # print(credit_details_before)
    credits_used_before = credit_details_before.get("data", {}).get("usage_monthly", 0)

    # 1. ask user to select a model (LLM)
    model_choice: str = input(
        "please choose a model from the below list:\n\n"
        f"{preset_models_str}\n\n"
        f"{CHAT_PREFIX} "
    )

    if model_choice not in preset_models:
        model_choice = DEFAULT_MODEL

    # 2. ask user for a prompt/question to answer
    user_prompt: str = input(f"hello, how can i help?\n\n{CHAT_PREFIX} ")

    # 3. invoke OpenRouter API for a response
    completion = open_router.chat.send(
        messages=[
            {
                "role": ROLE_USER,
                "content": user_prompt,
            },
        ],
        model=model_choice,
    )
    answer: str = str(completion.choices[0].message.content)
    print(f"{answer}\n\n")

    # 4. return response and billing + cost metadata
    credit_details_after: dict = get_credit_details()
    # print(credit_details_after)
    credits_used_after = credit_details_after.get("data", {}).get("usage_monthly", 0)
    request_cost: float = round(credits_used_after - credits_used_before, 6)
    print(f"credits used: ${request_cost:.4f} USD\n\n")

    time.sleep(3.0)


if __name__ == "__main__":

    demo_attempts = 3
    while demo_attempts > 0:

        try:
            result = query_user()

            if result == 1:
                exit(0)

            demo_attempts -= 1
        except Exception:
            logger.exception("Exception: ")
