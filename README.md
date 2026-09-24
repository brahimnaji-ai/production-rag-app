<h1 align="center">Production RAG App (Inngest-Based)</h1>

<p align="center">
  <a href="https://github.com/brahimnaji-ai/production-rag-app/actions/workflows/ci.yml"><img src="https://github.com/brahimnaji-ai/production-rag-app/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <img src="https://img.shields.io/badge/Python-3.14+-3776AB.svg?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-0.141+-009688.svg?logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/Inngest-Event--Driven-8B5CF6.svg" alt="Inngest">
  <img src="https://img.shields.io/badge/Qdrant-Vector%20DB-DC2626.svg" alt="Qdrant">
  <img src="https://img.shields.io/badge/Streamlit-1.64+-FF4B4B.svg?logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Google%20Gemini-GenAI-4285F4.svg?logo=google&logoColor=white" alt="Google Gemini">
  <a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff"></a>
  <a href="https://docs.astral.sh/uv/"><img src="https://img.shields.io/badge/managed%20by-uv-DE5FE9.svg" alt="uv"></a>
</p>

<p align="center">
  A robust, event-driven Retrieval-Augmented Generation (RAG) system built with <b>FastAPI</b>, <b>Inngest</b>, <b>Qdrant</b>, <b>Google Gemini</b>, <b>LlamaIndex</b>, and <b>Streamlit</b>.
</p>

---

## Architecture Overview

```
+--------------------------------------------------------------+
|                     Streamlit Web UI                         |
|   - Upload PDF Documents                                     |
|   - Ask Questions & View Citations                           |
+--------------+-------------------------------+---------------+
               | sends 'rag/ingest_pdf'        | sends 'rag/query_pdf_ai'
               | event                         | event & polls run output
               v                               v
+--------------------------------------------------------------+
|                    Inngest Dev Server                        |
|              (Durable Execution Engine)                      |
+------------------------------+-------------------------------+
                               | triggers steps
                               v
+--------------------------------------------------------------+
|                   FastAPI Webhook Server                     |
|                                                              |
|  [rag_ingest_pdf Function]                                   |
|   1. load-and-chunk-pdf: LlamaIndex PDFReader + Splitter     |
|   2. embed-and-upsert: Gemini Embeddings -> Qdrant           |
|                                                              |
|  [rag_query_pdf_ai Function]                                 |
|   1. embed-and-search: Query vector similarity search        |
|   2. llm-answer: ctx.step.ai.infer (Gemini 2.5 Flash)        |
+--------------+-------------------------------+---------------+
               |                               |
               v                               v
    +--------------------+           +--------------------+
    |   Qdrant Vector    |           |   Google Gemini    |
    |      Database      |           |     AI Engine      |
    |    (Port 6333)     |           | (Embeddings & LLM) |
    +--------------------+           +--------------------+
```

---

## Features

- **Durable Event-Driven Pipelines**: Uses Inngest step functions to make ingestion and inference workflows fault-tolerant, retryable, and observable.
- **Document Ingestion**: Extracts text from PDFs via `LlamaIndex` and segments it into semantic chunks with overlapping windows (`SentenceSplitter`).
- **High-Dimensional Embeddings**: Generates 3072-dimensional vector embeddings using Google GenAI `gemini-embedding-001`.
- **Fast Similarity Search**: Persists and indexes vectors in a containerized `Qdrant` instance with Cosine distance metric.
- **Contextual Generation**: Leverages Inngest's native AI adapter (`ctx.step.ai.infer`) with `gemini-2.5-flash` to synthesize accurate, context-grounded answers.
- **Interactive UI**: A Streamlit interface supporting multi-step PDF uploads and real-time query polling.
- **Type Safety**: Strictly validated step input/output models powered by Pydantic.

---

## Repository Structure

```
production-rag-app/
├── custom_types.py          # Pydantic models for step inputs, outputs, and contracts
├── data_loader.py           # PDF loader, text chunking, and Gemini embeddings
├── docker-compose.yaml      # Docker service definition for Qdrant vector database
├── main.py                  # Inngest functions, AI inference, and FastAPI serving
├── pyproject.toml           # Project dependencies, dev tools, and pytest configuration
├── streamlit_app.py         # Streamlit user interface
├── uv.lock                  # Pinned dependency lockfile
├── .github/workflows/       # GitHub Actions CI workflow (linting & testing)
└── tests/                   # Unit test suite
```

---

## Prerequisites

- [Python](https://www.python.org/) 3.14+
- [uv](https://docs.astral.sh/uv/) (Python package manager)
- [Docker](https://www.docker.com/) & Docker Compose
- [Node.js](https://nodejs.org/) (for Inngest Dev Server CLI: `npx inngest-cli`)
- A [Google Gemini API Key](https://aistudio.google.com/)

---

## Getting Started

### 1. Clone & Install Dependencies

```bash
git clone https://github.com/brahimnaji-ai/production-rag-app.git
cd production-rag-app
uv sync
```

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
INNGEST_API_BASE=http://127.0.0.1:8288/v1
```

### 3. Start Qdrant Vector Database

Start Qdrant using Docker Compose:

```bash
docker compose up -d
```

Verify that Qdrant is running at `http://localhost:6333` (Web Dashboard: `http://localhost:6333/dashboard`).

### 4. Start the Inngest Dev Server

Launch the Inngest dev server pointing to the FastAPI app:

```bash
npx inngest-cli@latest dev -u http://127.0.0.1:8000/api/inngest
```

The Inngest dashboard will be accessible at `http://127.0.0.1:8288`.

### 5. Start the FastAPI Server

Run the FastAPI application with Uvicorn:

```bash
uv run uvicorn main:app --reload --port 8000
```

### 6. Run the Streamlit Application

In a separate terminal, launch the Streamlit frontend:

```bash
uv run streamlit run streamlit_app.py
```

Open `http://localhost:8501` in your browser.

---

## Testing & Quality Assurance

### Run Unit Tests

```bash
uv run pytest
```

### Run Linter

```bash
uv run ruff check .
```

---

## Workflow Details

### 1. Ingestion (`rag/ingest_pdf`)
- **Trigger**: Fired when a PDF is uploaded through the Streamlit interface.
- **Step 1 (`load-and-chunk-pdf`)**: Reads the file from disk using `llama-index-readers-file` and splits text into 1,000-character chunks with a 200-character overlap.
- **Step 2 (`embed-and-upsert`)**: Computes embeddings via `gemini-embedding-001` and stores them in Qdrant with deterministic UUIDv5 IDs and metadata payloads (`source`, `text`).

### 2. Querying (`rag/query_pdf_ai`)
- **Trigger**: Fired when a user submits a question in Streamlit.
- **Step 1 (`embed-and-search`)**: Embeds the user question and retrieves top-$k$ relevant chunks from Qdrant.
- **Step 2 (`llm-answer`)**: Formats retrieved contexts into a prompt and calls `gemini-2.5-flash` using Inngest AI step inference. The run completes with the generated answer, source citations, and context metrics.
