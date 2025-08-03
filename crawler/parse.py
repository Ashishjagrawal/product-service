from bs4 import BeautifulSoup
import re

def parse_product_html(html: str, source_url: str) -> dict:
    soup = BeautifulSoup(html, "lxml")

    def text(sel):
        tag = soup.select_one(sel)
        return tag.text.strip() if tag else None

    name = text(".product_main h1")
    price_text = text(".product_main .price_color")
    price = float(re.sub(r"[^\d.]", "", price_text)) if price_text else None

    rating_str = None
    rating_tag = soup.select_one(".product_main p.star-rating")
    if rating_tag:
        for cls in rating_tag.attrs.get("class", []):
            if cls != "star-rating":
                rating_str = cls
    # Convert rating like 'Three' etc. to a numeric value
    rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    rating = rating_map.get(rating_str, None)

    description = None
    desc_tag = soup.select_one("#product_description ~ p")
    if desc_tag:
        description = desc_tag.text.strip()

    category = None
    cat_tag = soup.select_one(".breadcrumb li:nth-child(3) a")
    if cat_tag:
        category = cat_tag.text.strip()

    availability = text(".product_main .instock.availability")

    return {
        "name": name,
        "price": price,
        "rating": rating,
        "description": description,
        "url": source_url,
        "category": category,
        "availability": availability,
    }