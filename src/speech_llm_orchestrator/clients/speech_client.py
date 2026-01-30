import httpx
from fastapi import UploadFile, HTTPException


class SpeechClient:
    """
    Asynchronous client for interacting with a speech transcription service.

    The service is expected to expose a POST `/use-cases/transcribe` endpoint
    that accepts an audio file upload and returns a transcription result.
    """

    def __init__(self, base_url: str) -> None:
        """
        Initialize the speech client.

        Args:
            base_url: Base URL of the speech service. The scheme (`http://`
                or `https://`) will be added automatically if missing.
        """
        if not base_url.startswith(("http://", "https://")):
            base_url = "http://" + base_url

        self.base_url: str = base_url.rstrip("/")

    async def transcribe(self, file: UploadFile) -> str:
        """
        Transcribe an uploaded audio file using the speech service.

        Args:
            file: Audio file uploaded via FastAPI.

        Returns:
            The transcribed text.

        Raises:
            HTTPException: If the speech service returns a non-200 response
                or an invalid payload.
        """
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

        try:
            data = response.json()
            return data["transcript"]
        except (ValueError, KeyError) as exc:
            raise HTTPException(
                status_code=502,
                detail="Invalid response format from speech service",
            ) from exc
