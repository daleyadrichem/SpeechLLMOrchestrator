import os


def require_http_url(name: str, default: str) -> str:
    """
    Retrieve and validate an HTTP(S) base URL from environment variables.

    The value must begin with `http://` or `https://`. Trailing slashes
    are removed to ensure consistent URL construction elsewhere.

    Args:
        name: Environment variable name.
        default: Default value to use if the variable is not set.

    Returns:
        A normalized base URL with no trailing slash.

    Raises:
        RuntimeError: If the value does not start with a valid HTTP scheme.
    """
    value = os.getenv(name, default)

    if not value.startswith(("http://", "https://")):
        raise RuntimeError(f"{name} must include http:// or https:// — got: {value}")

    return value.rstrip("/")


# ---------------------------------------------------------------------------
# External service configuration
# ---------------------------------------------------------------------------

STT_BASE_URL: str = require_http_url(
    "STT_BASE_URL",
    "http://stt-api:8000",
)

LLM_BASE_URL: str = require_http_url(
    "LLM_BASE_URL",
    "http://llm-api:8000",
)
