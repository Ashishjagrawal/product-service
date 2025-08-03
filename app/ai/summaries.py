import os
import openai
from app.db.crud import get_product_summary, save_product_summary
from sqlalchemy.orm import Session
from dotenv import load_dotenv

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_summary_from_llm(text: str) -> str:
    prompt = (
        f"Create a catchy and persuasive one-liner to market the following product. "
        f"Highlight what makes it appealing or useful in under 40 words. "
        f"Use a consumer-friendly tone.\n\n"
        f"Details: {text}"
    )
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=60,
            temperature=0.8,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return "Excellent product to suit your needs."

def get_marketing_summary(db: Session, product_id: int, product_text: str) -> str:
    # Check cached summary
    cached_summary = get_product_summary(db, product_id)
    if cached_summary:
        return cached_summary
    
    # Generate new summary
    summary = generate_summary_from_llm(product_text)
    # Save cache
    save_product_summary(db, product_id, summary)
    return summary