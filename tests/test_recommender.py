import numpy as np

from src.recommender import top_unique_indices


def test_top_unique_indices_removes_duplicate_skus() -> None:
    scores = np.array([0.9, 0.8, 0.7, 0.6])
    skus = ["a", "a", "b", "c"]
    assert top_unique_indices(scores, skus, 3) == [0, 2, 3]

