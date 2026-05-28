# Personal Knowledge Base RAG Agent

A backend-only Python project scaffold for a personal knowledge base RAG Agent.

This project currently provides the base FastAPI structure, configuration, service placeholders, and a health check endpoint. Full RAG ingestion and retrieval workflows are intentionally not implemented yet.

## Tech Stack

- Python 3.10+
- FastAPI
- Chroma
- DeepSeek API
- PyMuPDF
- python-docx
- LangChain text splitter

## Project Structure

```text
.
├── app
│   ├── api
│   │   ├── routes
│   │   │   └── health.py
│   │   └── v1_router.py
│   ├── core
│   │   └── config.py
│   ├── database
│   │   └── chroma.py
│   ├── schemas
│   │   └── health.py
│   ├── services
│   │   ├── deepseek_service.py
│   │   ├── document_loader.py
│   │   └── text_splitter.py
│   └── main.py
├── .env.example
├── requirements.txt
└── README.md
```

## Installation

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

On Windows with Python 3.12, if Chroma's default `chroma-hnswlib` wheel crashes during vector writes, reinstall the verified wheel:

```bash
pip install --force-reinstall --no-deps chroma-hnswlib==0.7.5
```

## Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Configure the following values in `.env`:

```env
APP_NAME=Personal Knowledge Base RAG Agent
APP_ENV=development
API_V1_PREFIX=/api/v1

DEEPSEEK_API_KEY=your_deepseek_api_key
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-chat

CHROMA_PERSIST_DIRECTORY=backend/vector_db
CHROMA_COLLECTION_NAME=personal_knowledge_base
```

## Run

Start the development server:

```bash
uvicorn app.main:app --reload
```

Health check:

```bash
curl http://127.0.0.1:8000/health
```

or:

```bash
curl http://127.0.0.1:8000/api/v1/health
```

Expected response:

```json
{
  "status": "ok",
  "service": "Personal Knowledge Base RAG Agent"
}
```

## Current Scope

Implemented:

- FastAPI application factory
- `/health` and `/api/v1/health`
- Pydantic settings
- Chroma client helper
- DeepSeek service placeholder
- PDF/DOCX/text loader placeholder
- LangChain text splitter helper

Not implemented yet:

- File upload API
- Document indexing workflow
- Embedding model integration
- Retrieval and answer generation
- Conversation/session storage
