from pydantic import BaseModel, Field


class TranscriptResponse(BaseModel):
    """
    Response model containing a raw transcript.
    """

    transcript: str = Field(
        ...,
        description="Full text transcript generated from audio input.",
    )


class SummaryResponse(BaseModel):
    """
    Response model containing a transcript and its generated summary.
    """

    transcript: str = Field(
        ...,
        description="Original transcript text.",
    )
    summary: str = Field(
        ...,
        description="Condensed summary derived from the transcript.",
    )


class AskRequest(BaseModel):
    """
    Request model for asking a question about a transcript.
    """

    transcript: str = Field(
        ...,
        description="Transcript text used as the knowledge source.",
    )
    question: str = Field(
        ...,
        description="Question to be answered based on the transcript.",
    )


class AskResponse(BaseModel):
    """
    Response model containing an answer generated from a transcript.
    """

    transcript: str = Field(
        ...,
        description="Original transcript text used to generate the answer.",
    )
    answer: str = Field(
        ...,
        description="Answer generated from the transcript context.",
    )
