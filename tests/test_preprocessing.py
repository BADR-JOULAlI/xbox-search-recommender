from src.preprocessing import coerce_sku, normalize_query, normalize_text


def test_normalize_text_preserves_words() -> None:
    assert normalize_text("  Call-of-Dúty_ 4! ") == "call of duty 4"


def test_normalize_query_collapses_format_variants() -> None:
    expected = "rocksmith1"
    assert normalize_query("Rock Smith_1") == expected
    assert normalize_query("rock-smith 1") == expected


def test_coerce_sku_removes_csv_float_suffix() -> None:
    assert coerce_sku("9854804.0") == "9854804"
    assert coerce_sku("SKU-01") == "SKU-01"

