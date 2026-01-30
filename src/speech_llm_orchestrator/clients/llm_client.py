import httpx
from fastapi import HTTPException


class LLMClient:
    def __init__(self, base_url: str):
        if not base_url.startswith(("http://", "https://")):
            base_url = "http://" + base_url

        self.base_url = base_url.rstrip("/")

        print("LLMClient base url:", self.base_url)

    async def generate(
        self,
        prompt: str,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> str:
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

        return response.json()["response"]
