# Product Microservice

A scalable Python microservice that asynchronously crawls product data from an e‑commerce domain, persists it reliably, and exposes AI-driven insights via a FastAPI JSON REST API. The service includes embedding-based similarity recommendations, AI-generated marketing summaries, and rich analytics.

---

## Table of Contents

- [Overview](#overview)
- [Setup Instructions](#setup-instructions)
- [Database Setup and Migrations](#database-setup-and-migrations)
- [Environment Variables](#environment-variables)
- [Running the Application](#running-the-application)
- [Testing](#testing)
- [Docker and Containerization](#docker-and-containerization)
- [Architecture Decisions](#architecture-decisions)
- [Scaling and Performance Considerations](#scaling-and-performance-considerations)
- [Documentation and Diagrams](#documentation-and-diagrams)

---

## Overview

This microservice performs:

- Asynchronous web crawling of product pages.
- Parsing and normalizing product data for storage.
- Generation of lightweight product embeddings for similarity search.
- Calling an LLM (OpenAI GPT-3.5) to generate concise marketing summaries with cache.
- Serving data and AI insights through a FastAPI REST interface.
- Robust request validation and error handling.
- Containerized deployment and automated CI pipeline.

---

## Setup Instructions

### Prerequisites

- Python 3.11+
- Docker and Docker Compose (optional but recommended)
- An OpenAI API key for marketing summaries
- Git

### Install Dependencies

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

### Crawling and Data Ingestion

1. Crawl publicly accessible product pages:

```bash
python -m crawler.crawl
```

2. Parse raw HTML and seed the database:

```bash
python -m crawler.parse_and_insert
```

3. Generate embeddings and marketing summaries:

```bash
python generate_embeddings_and_summaries.py
```

---

### Running the API Server

```bash
uvicorn app.main:app --reload
```

The API documentation is available at:  
[http://localhost:8000/docs](http://localhost:8000/docs)

---

## Database Setup and Migrations

This project manages database schema with SQLAlchemy ORM and Alembic migrations.

### Install Alembic

```bash
pip install alembic
```

### Apply Migrations

Configure your environment variable `DATABASE_URL`:

```bash
export DATABASE_URL=sqlite:///./products.db
# or for PostgreSQL
# export DATABASE_URL=postgresql://user:password@localhost:5432/products
```

Then run the migrations:

```bash
alembic upgrade head
```

### Creating New Migrations

After modifying models, generate and apply new migrations:

```bash
alembic revision --autogenerate -m "Describe migration"
alembic upgrade head
```

---

## Environment Variables

The service requires:

| Variable       | Description                                   | Example                               |
|----------------|-----------------------------------------------|-------------------------------------|
| `DATABASE_URL` | Database connection string (SQLite/Postgres) | `sqlite:///./products.db`            |
| `OPENAI_API_KEY` | OpenAI API key for marketing summary generation | `sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx`  |

Place these in a `.env` file for local development (auto-loaded via `python-dotenv`):

```env
DATABASE_URL=sqlite:///./products.db
OPENAI_API_KEY=your_openai_api_key_here
```

---

## Testing

Run the full test suite with:

```bash
pytest --disable-warnings -v
```

Tests cover:

- Crawler parsing logic.
- Embedding and similarity computations.
- Marketing summary generation (with LLM API mocked).
- CRUD database interactions.
- FastAPI API integration.

All tests use an isolated in-memory database and mock external API calls for consistency.

---

## Docker and Containerization

### Build the Docker image:

```bash
docker build -t product_service:latest .
```

### Run the container locally:

```bash
docker run -p 8000:8000 -v $(pwd)/data:/app/data product_service:latest
```

### Alternatively, use Docker Compose:

```bash
docker-compose up --build
```

---

## Architecture Decisions

- **FastAPI:** Asynchronous API framework allowing high throughput and automatic docs.
- **SQLAlchemy + Alembic:** ORM and migration framework offering database abstraction and seamless schema evolution.
- **aiohttp + asyncio:** Efficient asynchronous web crawling with concurrency control.
- **sentence-transformers:** Lightweight and effective embeddings for semantic similarity.
- **OpenAI GPT-3.5:** AI-generated marketing summaries, cached to reduce API calls and latency.
- **Docker & GitHub Actions:** Containerization and CI/CD pipeline for consistent deployment and automated testing.

Clear modular structure enables separation of crawling, storage, AI insight extraction, and API serving.

---

## Scaling and Performance Considerations

### Code/Architecture Level

- **Async APIs and Crawlers:** Non-blocking concurrency to maximize throughput; deploy with async web servers.
- **Modular AI Layer:** Support swapping embedding models or LLM providers easily.
- **Cache AI outputs aggressively:** Avoid redundant LLM calls by persistent caching of summaries & recommendations.

### Data Layer

- **Database:** Use PostgreSQL in production for better indexing, partitioning, and large-scale storage.
- **Feature Store:** Introduce a dedicated feature store service (e.g., Feast) as dataset grows for AI feature management.
- **Batch vs Streaming:** Move from batch crawling to streaming pipelines (Kafka, RabbitMQ) for real-time updates.

### Infrastructure

- **Horizontal Scalability:** Containerize microservices; deploy with Kubernetes or managed orchestration.
- **Distributed Similarity Search:** Replace in-memory cosine with Faiss or Annoy for large datasets.
- **Scaling AI workloads:** Cache embeddings and summaries; offload expensive AI computations to async workers or serverless functions.
- **Global API scaling:** Multi-region deployment with CDN and global load balancing for low-latency user access.

### Latency & Efficiency

- **Use async I/O throughout** API, crawler, and AI calls to maximize resource efficiency and minimize delays.
- **Cache layer:** Use Redis or Memcached for summaries and recommendation results.
- **Batch AI calls** where possible to optimize throughput over latency.
- **Database indexing:** Optimize indexes based on query patterns (e.g., price, rating).

---

## Documentation and Diagrams

See `/docs` folder for:

- **Architecture Diagrams:** Visual representation of the components and data flow.
- **Deployment Diagrams:** Container architecture and CI/CD process.
- **Data Flow Diagrams:** Step-by-step data processing from crawl to AI insights serving.
