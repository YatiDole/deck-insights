from ops_deck_rag.extractors import safe_text


def test_safe_text_handles_none():
    assert safe_text(None) == ""


def test_safe_text_strips():
    assert safe_text("  hello  ") == "hello"
