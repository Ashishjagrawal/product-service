from unittest.mock import patch
import pytest
from app.db.models import Product
from app.ai.summaries import generate_summary_from_llm, get_marketing_summary
from app.ai import summaries

@patch("app.ai.summaries.client.chat.completions.create")
def test_generate_summary_from_llm(mock_openai_create):
    mock_openai_create.return_value = type(
        "MockResp", (), 
        {"choices": [type("Choice", (), {"message": type("Msg", (), {"content": "Mock summary"})()})()]}
    )()
    
    from app.ai.summaries import generate_summary_from_llm
    result = generate_summary_from_llm("any text")
    
    assert result == "Mock summary"

@patch("app.ai.summaries.generate_summary_from_llm")
def test_get_marketing_summary_caches(mock_gen_summary, db_session):
    mock_gen_summary.return_value = "cached summary"

    # Provide all required fields; price non-null and others as plain defaults
    product = Product(
        id=1,
        name="Test",
        price=10.0,  # must provide non-nullable price
        rating=4.0,
        description="Test description",
        url="http://example.com/test-product",
        category="Test Category",
        availability="In stock",
        marketing_summary="cached summary",
    )
    db_session.add(product)
    db_session.commit()

    summary = get_marketing_summary(db_session, 1, "desc")
    assert summary == "cached summary"

    mock_gen_summary.reset_mock()
    summary2 = get_marketing_summary(db_session, 1, "desc")
    assert summary2 == "cached summary"

    mock_gen_summary.assert_not_called()