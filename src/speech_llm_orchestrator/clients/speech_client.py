import httpx
from fastapi import UploadFile, HTTPException


class SpeechClient:
    def __init__(self, base_url: str):
        if not base_url.startswith(("http://", "https://")):
            base_url = "http://" + base_url

        self.base_url = base_url.rstrip("/")

        print("SpeechClient base url:", self.base_url)

    async def transcribe(self, file: UploadFile) -> str:
        async with httpx.AsyncClient(timeout=600) as client:
            response = await client.post(
                f"{self.base_url}/use-cases/transcribe",
                files={
                    "file": (
                        file.filename,
                        await file.read(),
                        file.content_type,
                    )
                },
            )

        if response.status_code != 200:
            raise HTTPException(
                status_code=502,
                detail=f"Speech service error: {response.text}",
            )

        return response.json()["transcript"]
