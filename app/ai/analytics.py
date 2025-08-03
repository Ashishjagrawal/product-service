from sqlalchemy import text
from collections import Counter, defaultdict
import nltk
from nltk.corpus import stopwords
from nltk import word_tokenize, pos_tag
import re

# Download once before using
# nltk.download('averaged_perceptron_tagger')
# nltk.download('punkt')
# nltk.download('stopwords')
import spacy

# Load once (module-level)
nlp = spacy.load("en_core_web_sm")

STOP_WORDS = set(stopwords.words('english'))

def extract_adjectives(text: str):
    if not text:
        return []
    doc = nlp(text.lower())
    # Extract adjectives (POS tag 'ADJ')
    adjectives = [token.text for token in doc if token.pos_ == "ADJ"]
    return adjectives

def get_trends(db):
    # Get average price by rating (1-5 stars)
    rating_prices = db.execute(text("""
        SELECT rating, AVG(price) as avg_price, COUNT(*) as cnt
        FROM products
        WHERE rating IS NOT NULL
        GROUP BY rating
        ORDER BY rating
    """)).fetchall()

    price_by_rating = [{"rating": int(r), "average_price": float(p), "count": c} for r, p, c in rating_prices]

    # Get all descriptions
    descriptions = db.execute(text("SELECT description FROM products WHERE description IS NOT NULL")).fetchall()

    # Accumulate adjectives across all descriptions
    all_adjectives = []
    for (desc,) in descriptions:
        adjectives = extract_adjectives(desc)
        all_adjectives.extend(adjectives)

    top_adjectives = Counter(all_adjectives).most_common(5)

    # Get average price by category and count
    category_stats = db.execute(text("""
        SELECT category, COUNT(*) as cnt, AVG(price) as avg_price
        FROM products
        WHERE category IS NOT NULL
        GROUP BY category
        ORDER BY cnt DESC
        LIMIT 5
    """)).fetchall()

    categories = [{"category": cat, "count": cnt, "average_price": float(avgp)} for cat, cnt, avgp in category_stats]

    return {
        "price_by_rating": price_by_rating,
        "top_adjectives": [{"adjective": adj, "count": cnt} for adj, cnt in top_adjectives],
        "top_categories": categories
    }