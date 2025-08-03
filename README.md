# 🛍️ Product Microservice

## Overview

This microservice asynchronously crawls product data from [books.toscrape.com](http://books.toscrape.com), persists it reliably, generates semantic embeddings and AI-driven marketing summaries, and exposes a FastAPI-based JSON REST API for accessing products and analytics insights.

---

## 🚀 Features

- Asynchronous web scraping using `aiohttp` and `asyncio`
- SQLite (dev) / PostgreSQL (prod-ready) via SQLAlchemy ORM
- AI embeddings using `sentence-transformers`
- Marketing copy generation using OpenAI GPT-3.5
- FastAPI server with auto-generated Swagger docs
- Dockerized architecture for reproducible deployments
- CI-ready via GitHub Actions (optional)
- Modular and production-ready code structure

---

## ⚙️ Setup Instructions

### Prerequisites

- Python 3.11+
- [Docker](https://www.docker.com/) & Docker Compose (optional but recommended)
- OpenAI API key (for marketing summaries)
- [Optional] PostgreSQL (recommended for production)

---

### 🧪 Local Development

```bash
# 1. Create and activate virtual environment
python -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt
````

---

### 🕸️ Run the Crawler

Fetch product HTML pages asynchronously:

```bash
python -m crawler.crawl
```

Parse and insert product data into the database:

```bash
python -m crawler.parse_and_insert
```

---

### 🤖 Generate AI Insights

```bash
python generate_embeddings_and_summaries.py
```

---

### 🚦 Start the API Server

```bash
uvicorn app.main:app --reload
```

Visit the interactive API docs at:
📄 [http://localhost:8000/docs](http://localhost:8000/docs)

---

### ✅ Run Tests

```bash
pytest --disable-warnings -v
```

---

## 🐳 Docker Usage

### Build Container

```bash
docker build -t product_service:latest .
```

### Run Container

```bash
docker run -p 8000:8000 product_service:latest
```

### Docker Compose

```bash
docker-compose up --build
```

---

## 🧱 Architectural Decisions

### Technology Choices

* **FastAPI**: High-performance async web framework with built-in OpenAPI support
* **SQLAlchemy + Alembic**: Flexible ORM + migrations; supports SQLite and PostgreSQL
* **aiohttp + asyncio**: Efficient and scalable async crawling
* **sentence-transformers**: For generating lightweight semantic embeddings
* **OpenAI GPT-3.5**: For concise marketing copy with response caching
* **Docker**: Containerized development and deployment
* **GitHub Actions** *(optional)*: For CI automation

---

## 🧠 Design Principles

* Clear modular structure: crawler, parser, DB layer, API, AI insights
* Validation with **Pydantic** models for data integrity
* Idempotency and caching to reduce redundant LLM calls
* Fully asynchronous for scalability and responsiveness
* Separation of data ingestion, persistence, and analytics

---

## 📈 Scaling Strategies

* **Database**: Use PostgreSQL with indexing, partitioning, or hosted cloud DBs
* **Caching**: Integrate Redis for summaries, HTML, and similarity results
* **Similarity Search**: Move to FAISS or Annoy for scalable vector search
* **API Scaling**: Container orchestration with Kubernetes, HPA, and Ingress controllers
* **Embedding & Summarization**: Offload to background workers (Celery, Kafka)
* **Monitoring**: Add tracing, log aggregation, and metrics dashboards (e.g., Prometheus + Grafana)

---

## 📬 Contact

For questions or contributions, open an issue or PR on this repo. Happy coding!

```
