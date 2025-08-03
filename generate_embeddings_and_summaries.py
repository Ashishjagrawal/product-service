from app.db.database import SessionLocal
from app.ai.embeddings import generate_and_store_embeddings_and_summaries

def main():
    db = SessionLocal()
    try:
        generate_and_store_embeddings_and_summaries(db)
    finally:
        db.close()

if __name__ == "__main__":
    main()