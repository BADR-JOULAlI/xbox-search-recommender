import pytest

from src.metrics import average_precision_at_k, evaluate_rankings


def test_average_precision_at_five() -> None:
    assert average_precision_at_k({"a"}, ["x", "a", "b"], 5) == pytest.approx(0.5)


def test_metrics_ignore_duplicate_predictions() -> None:
    metrics = evaluate_rankings([{"a", "b"}], [["a", "a", "x", "b"]], 5)
    assert metrics["recall@5"] == 1.0
    assert metrics["hit_rate@5"] == 1.0


def test_metrics_reject_misaligned_batches() -> None:
    with pytest.raises(ValueError):
        evaluate_rankings([{"a"}], [], 5)

