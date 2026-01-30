# Speech LLM Orchestrator

This repository contains the **Speech–LLM Orchestrator** service.

The orchestrator is a lightweight FastAPI service that coordinates:

- 🎙️ Speech-to-Text (audio/video transcription)
- 🧠 Local LLM reasoning (summarization, Q&A, description)

It does **not** run any ML models itself.

Instead, it connects to two existing containers:

- a **Speech-to-Text API**
- a **Local LLM API**

---

## Architecture

```

```
            ┌──────────────────────┐
            │  Client / Frontend   │
            └──────────┬───────────┘
                       │
                       ▼
          ┌──────────────────────────┐
          │ Speech LLM Orchestrator  │
          │        (this repo)       │
          │                          │
          │  - /transcribe           │
          │  - /summarize            │
          │  - /ask                  │
          └──────────┬───────────────┘
                     │
    ┌────────────────┴───────────────┐
    │                                │
    ▼                                ▼
```

┌────────────────────┐        ┌────────────────────┐
│ Speech-to-Text API │        │   Local LLM API    │
│ (Whisper / etc.)   │        │ (Ollama wrapper)   │
└────────────────────┘        └────────────────────┘

```

---

## ⚠️ Important

**This repository cannot run by itself.**

You must first build the Docker images from the following two repositories:

- **Speech-to-Text API**
```

[Audio Transcription demo](https://github.com/daleyadrichem/AudioTranscriptionDemo)

```

- **Local LLM API**
```

[Local LLM demo](https://github.com/daleyadrichem/LocalLLMDemo)

````

The orchestrator expects those images to already exist locally.

---

## Required Docker Images

Before running this repo, the following images must be available:

| Service | Docker image |
|------|------|
| Speech-to-Text API | `audiotranscriptiondemo-app:latest` |
| Local LLM API | `localllmdemo-app:latest` |
| Ollama backend | `ollama/ollama:latest` |

If these images are missing, Docker Compose will fail to start.

---

## Build dependencies first

### 1️⃣ Build Speech-to-Text container

```bash
git clone https://github.com/daleyadrichem/AudioTranscriptionDemo
cd speech-to-text-repo

docker build -t audiotranscriptiondemo-app:latest .
````

---

### 2️⃣ Build Local LLM container

```bash
git clone https://github.com/daleyadrichem/LocalLLMDemo
cd local-llm-repo

docker build -t localllmdemo-app:latest .
```

---

### 3️⃣ Verify images exist

```bash
docker images | grep demo
```

You should see something similar to:

```
audiotranscriptiondemo-app   latest
localllmdemo-app             latest
```

---

## Running the orchestrator

Once both images exist:

```bash
docker compose up
```

The compose file will start:

* Speech-to-Text API
* Local LLM API
* Ollama backend
* Speech LLM Orchestrator

---

## Exposed services

| Service              | URL                                                      |
| -------------------- | -------------------------------------------------------- |
| Orchestrator API     | [http://localhost:9000](http://localhost:9000)           |
| Orchestrator Swagger | [http://localhost:9000/docs](http://localhost:9000/docs) |
| Speech-to-Text API   | [http://localhost:8000](http://localhost:8000)           |
| Local LLM API        | [http://localhost:8001](http://localhost:8001)           |
| Ollama               | [http://localhost:11434](http://localhost:11434)         |

---

## API Endpoints

### `POST /transcribe`

Upload audio or video and receive a transcription.

**Input**

* multipart file upload

**Output**

```json
{
  "transcript": "..."
}
```

---

### `POST /summarize`

Upload audio or video and receive:

* transcription
* LLM-generated summary

**Output**

```json
{
  "transcript": "...",
  "summary": "..."
}
```

---

### `POST /ask`

Upload audio or video and ask a question about the content.

**Form fields**

* `file`: audio/video file
* `question`: natural language question

**Output**

```json
{
  "transcript": "...",
  "answer": "..."
}
```

---

## Environment variables

The orchestrator communicates with other containers via Docker DNS.

Default values:

```env
STT_BASE_URL=http://stt-api:8000
LLM_BASE_URL=http://llm-api:8000
```

These normally do not need to be changed.

---

## Technology stack

* Python 3.11
* FastAPI
* httpx (async HTTP)
* Docker & Docker Compose
* uv / uvicorn
* Ollama (LLM backend)

---

## Design principles

* No models inside the orchestrator
* Clear separation of concerns
* Microservice-friendly architecture
* Async-only networking
* Container-to-container communication (no localhost coupling)

---

## Future extensions

This architecture makes it easy to add:

* Vector embeddings + RAG
* Long-audio chunking
* Speaker diarization
* Streaming transcription
* Background task processing
* Persistent transcript storage

---

## License

MIT