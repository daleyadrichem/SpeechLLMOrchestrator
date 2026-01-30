import httpx
from fastapi import HTTPException


class LLMClient:
    """
    Asynchronous client for interacting with an LLM inference service.

    The service is expected to expose a POST `/generate` endpoint that
    accepts a JSON payload containing a prompt and optional generation
    parameters.
    """

    def __init__(self, base_url: str) -> None:
        """
        Initialize the LLM client.

        Args:
            base_url: Base URL of the LLM service. The scheme (`http://`
                or `https://`) will be added automatically if missing.
        """
        if not base_url.startswith(("http://", "https://")):
            base_url = "http://" + base_url

        self.base_url: str = base_url.rstrip("/")

    async def generate(
        self,
        prompt: str,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> str:
        """
        Generate a completion from the LLM service.

        Args:
            prompt: Input prompt to send to the language model.
            temperature: Optional sampling temperature.
            max_tokens: Optional maximum number of tokens to generate.

        Returns:
            The generated text response from the LLM.

        Raises:
            HTTPException: If the LLM service returns a non-200 response
                or an invalid payload.
        """
        payload = {
            "prompt": prompt,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        async with httpx.AsyncClient(timeout=600) as client:
            response = await client.post(
                f"{self.base_url}/generate",
                json=payload,
            )

        if response.status_code != 200:
            raise HTTPException(
                status_code=502,
                detail=f"LLM service error: {response.text}",
            )

        try:
            data = response.json()
            return data["response"]
        except (ValueError, KeyError) as exc:
            raise HTTPException(
                status_code=502,
                detail="Invalid response format from LLM service",
            ) from exc
