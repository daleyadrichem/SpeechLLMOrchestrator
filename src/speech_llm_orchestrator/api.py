from fastapi import FastAPI, UploadFile, File, Form

from speech_llm_orchestrator.config import STT_BASE_URL, LLM_BASE_URL
from speech_llm_orchestrator.clients.speech_client import SpeechClient
from speech_llm_orchestrator.clients.llm_client import LLMClient
from speech_llm_orchestrator.models.schemas import (
    TranscriptResponse,
    SummaryResponse,
    AskResponse,
)


app = FastAPI(
    title="Speech Orchestrator",
    version="1.0.0",
    description="Orchestrates speech-to-text and LLM services.",
)

# ---------------------------------------------------------------------------
# Clients
# ---------------------------------------------------------------------------

speech_client = SpeechClient(STT_BASE_URL)
llm_client = LLMClient(LLM_BASE_URL)

# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@app.post("/transcribe", response_model=TranscriptResponse)
async def transcribe(file: UploadFile = File(...)) -> TranscriptResponse:
    """
    Transcribe an uploaded audio file.

    Args:
        file: Audio file uploaded by the client.

    Returns:
        TranscriptResponse containing the generated transcript.
    """
    transcript = await speech_client.transcribe(file)
    return TranscriptResponse(transcript=transcript)


@app.post("/summarize", response_model=SummaryResponse)
async def summarize(file: UploadFile = File(...)) -> SummaryResponse:
    """
    Transcribe an uploaded audio file and generate a summary.

    Args:
        file: Audio file uploaded by the client.

    Returns:
        SummaryResponse containing the transcript and its summary.
    """
    transcript = await speech_client.transcribe(file)

    prompt = f"""
Summarize the following transcript clearly:

{transcript}
"""

    summary = await llm_client.generate(prompt)

    return SummaryResponse(
        transcript=transcript,
        summary=summary,
    )


@app.post("/ask", response_model=AskResponse)
async def ask(
    file: UploadFile = File(...),
    question: str = Form(...),
) -> AskResponse:
    """
    Ask a question about the contents of an audio transcript.

    The answer is generated strictly from the transcript text.
    If the transcript does not contain the answer, the model
    is instructed to say so.

    Args:
        file: Audio file uploaded by the client.
        question: Question to ask about the transcript.

    Returns:
        AskResponse containing the transcript and generated answer.
    """
    # 1. Transcribe audio
    transcript = await speech_client.transcribe(file)

    # 2. Query the LLM using transcript context
    prompt = f"""
You are answering questions about an audio or video transcript.

Transcript:
{transcript}

Question:
{question}

Answer only using information present in the transcript.
If the transcript does not contain the answer, say so.
"""

    answer = await llm_client.generate(prompt)

    return AskResponse(
        transcript=transcript,
        answer=answer,
    )
