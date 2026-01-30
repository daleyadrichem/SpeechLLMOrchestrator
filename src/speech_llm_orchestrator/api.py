from fastapi import FastAPI, UploadFile, File, Form

from speech_llm_orchestrator.config import STT_BASE_URL, LLM_BASE_URL
from speech_llm_orchestrator.clients.speech_client import SpeechClient
from speech_llm_orchestrator.clients.llm_client import LLMClient
from speech_llm_orchestrator.models.schemas import (
    TranscriptResponse,
    SummaryResponse,
    AskResponse,
)
print("STT_BASE_URL =", STT_BASE_URL)
print("LLM_BASE_URL =", LLM_BASE_URL)
app = FastAPI(
    title="Speech Orchestrator",
    version="1.0.0",
)

speech_client = SpeechClient(STT_BASE_URL)
llm_client = LLMClient(LLM_BASE_URL)


@app.post("/transcribe", response_model=TranscriptResponse)
async def transcribe(file: UploadFile = File(...)):
    transcript = await speech_client.transcribe(file)
    return TranscriptResponse(transcript=transcript)


@app.post("/summarize", response_model=SummaryResponse)
async def summarize(file: UploadFile = File(...)):
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
):
    # 1️⃣ Transcribe
    transcript = await speech_client.transcribe(file)

    # 2️⃣ Ask LLM about transcript
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
