import os
import pytest
from crawler.parse import parse_product_html

@pytest.fixture
def sample_html():
    path = os.path.join(os.path.dirname(__file__), "fixtures/sample_product.html")
    with open(path, encoding="utf8") as f:
        return f.read()

def test_parse_product_html(sample_html):
    product = parse_product_html(sample_html, "http://example.com/book")
    assert product["name"] == "A Light in the Attic"
    assert product["price"] == 51.77
    assert product["rating"] == 3