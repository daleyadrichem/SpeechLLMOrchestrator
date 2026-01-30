import os


def require_http_url(name: str, default: str) -> str:
    value = os.getenv(name, default)

    if not value.startswith("http://") and not value.startswith("https://"):
        raise RuntimeError(
            f"{name} must include http:// or https:// — got: {value}"
        )

    return value.rstrip("/")


STT_BASE_URL = require_http_url(
    "STT_BASE_URL",
    "http://stt-api:8000",
)

LLM_BASE_URL = require_http_url(
    "LLM_BASE_URL",
    "http://llm-api:8000",
)
