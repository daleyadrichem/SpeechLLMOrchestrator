from pydantic import BaseModel


class TranscriptResponse(BaseModel):
    transcript: str


class SummaryResponse(BaseModel):
    transcript: str
    summary: str


class AskRequest(BaseModel):
    transcript: str
    question: str


class AskResponse(BaseModel):
    transcript: str
    answer: str
