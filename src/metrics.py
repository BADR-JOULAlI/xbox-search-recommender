"""Ranking metrics used consistently across notebooks and tests."""

from __future__ import annotations

from collections.abc import Hashable, Iterable, Sequence


def _unique_at_k(values: Sequence[Hashable], k: int) -> list[Hashable]:
    seen: set[Hashable] = set()
    unique: list[Hashable] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            unique.append(value)
        if len(unique) == k:
            break
    return unique


def average_precision_at_k(
    relevant: Iterable[Hashable], predicted: Sequence[Hashable], k: int = 5
) -> float:
    """Average precision at k for one query with one or more relevant items."""
    relevant_set = set(relevant)
    if not relevant_set:
        return 0.0
    hits = 0
    score = 0.0
    for rank, item in enumerate(_unique_at_k(predicted, k), start=1):
        if item in relevant_set:
            hits += 1
            score += hits / rank
    return score / min(len(relevant_set), k)


def evaluate_rankings(
    actual: Sequence[Iterable[Hashable]],
    predicted: Sequence[Sequence[Hashable]],
    k: int = 5,
) -> dict[str, float]:
    """Return MAP, recall, reciprocal rank, and hit rate at k."""
    if len(actual) != len(predicted):
        raise ValueError("actual et predicted doivent avoir la même longueur")
    if not actual:
        return {f"map@{k}": 0.0, f"recall@{k}": 0.0, f"mrr@{k}": 0.0, f"hit_rate@{k}": 0.0}

    ap_values: list[float] = []
    recalls: list[float] = []
    reciprocal_ranks: list[float] = []
    hits: list[float] = []
    for relevant, ranking in zip(actual, predicted, strict=True):
        relevant_set = set(relevant)
        top = _unique_at_k(ranking, k)
        matched = relevant_set.intersection(top)
        ap_values.append(average_precision_at_k(relevant_set, top, k))
        recalls.append(len(matched) / len(relevant_set) if relevant_set else 0.0)
        first_rank = next((rank for rank, item in enumerate(top, 1) if item in relevant_set), None)
        reciprocal_ranks.append(1.0 / first_rank if first_rank else 0.0)
        hits.append(float(bool(matched)))

    def mean(values: Sequence[float]) -> float:
        return sum(values) / len(values)

    return {
        f"map@{k}": mean(ap_values),
        f"recall@{k}": mean(recalls),
        f"mrr@{k}": mean(reciprocal_ranks),
        f"hit_rate@{k}": mean(hits),
    }
