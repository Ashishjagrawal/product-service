import os
import glob
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))  # To ensure app import works if run directly
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
# Construct absolute path for SQLite DB file
SQLITE_DB_PATH = os.path.join(BASE_DIR, "products.db")
DB_URL = os.getenv("DATABASE_URL", f"sqlite:///{SQLITE_DB_PATH}")
print(f"Using DB URL: {DB_URL}")
from app.db.database import SessionLocal
from app.db.crud import get_or_create_product
from .parse import parse_product_html

RAW_DIR = os.path.join(os.path.dirname(__file__), "../data/raw_html")

# def process_and_insert():
#     files = glob.glob(os.path.join(RAW_DIR, "*.html"))
#     print(f"Found {len(files)} HTML files to parse and insert.")
#     db = SessionLocal()
#     count = 0
#     for fpath in files:
#         with open(fpath, encoding="utf8") as f:
#             html = f.read()
#         # If you saved the url elsewhere, restore it, else use fpath
#         # Could reconstruct/record source_url earlier if wanted
#         source_url = "unknown"
#         prod = parse_product_html(html, source_url)
#         if not prod["url"]:
#             prod["url"] = fpath  # fallback
#         try:
#             existing = get_or_create_product(db, prod)
#             count += 1
#             print(f"Inserted/found: {prod['name']}")
#         except Exception as e:
#             print(f"Error inserting {prod.get('name') or fpath}: {e}")
#             db.rollback()
#     db.close()
#     print(f"Completed inserting/finding {count} products.")

def process_and_insert():
    files = glob.glob(os.path.join(RAW_DIR, "*.html"))
    print(f"Found {len(files)} HTML files to parse and insert.")
    db = SessionLocal()
    count = 0
    inserted_urls = set()
    for fpath in files:
        with open(fpath, encoding="utf8") as f:
            html = f.read()
        prod = parse_product_html(html, fpath)  # Pass filename as source_url

        # Defensive fallback for URL
        if not prod.get("url"):
            prod["url"] = fpath

        print(f"Processing product: Name='{prod.get('name')}', URL='{prod.get('url')}'")

        # Check duplicates in this session (optional)
        if prod["url"] in inserted_urls:
            print(f"Skipping duplicate URL in process: {prod['url']}")
            continue
        inserted_urls.add(prod["url"])

        try:
            instance = get_or_create_product(db, prod)
            count += 1
            print(f"Inserted/found: {instance.name}")
        except Exception as e:
            print(f"Error inserting {prod.get('name')}: {e}")
            db.rollback()
    db.close()
    print(f"Inserted/found total {count} products.")

if __name__ == "__main__":
    process_and_insert()