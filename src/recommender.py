"""Production inference wrapper around notebook-generated artifacts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import faiss
import joblib
import numpy as np
import pandas as pd
import torch
from sentence_transformers import SentenceTransformer

from src.artifact_loader import validate_manifest
from src.preprocessing import normalize_query, normalize_text


def top_unique_indices(scores: np.ndarray, skus: list[str], k: int) -> list[int]:
    """Return stable score-sorted positions while preventing duplicate SKUs."""
    order = np.argsort(-np.asarray(scores), kind="stable")
    selected: list[int] = []
    seen: set[str] = set()
    for position in order:
        sku = str(skus[int(position)])
        if sku not in seen:
            seen.add(sku)
            selected.append(int(position))
        if len(selected) == k:
            break
    return selected


class HybridRecommender:
    """Load persisted lexical, semantic, click-history, and popularity signals."""

    def __init__(self, artifact_dir: Path, device: str | None = None) -> None:
        self.artifact_dir = Path(artifact_dir)
        manifest_path = self.artifact_dir / "manifest.json"
        if manifest_path.exists():
            errors = validate_manifest(self.artifact_dir, manifest_path)
            if errors:
                raise ValueError(f"Artefacts invalides : {errors}")

        self.products = pd.read_csv(
            self.artifact_dir / "products.csv", dtype={"sku": str}
        ).fillna("")
        self.skus = self.products["sku"].astype(str).tolist()
        self.sku_to_position = {sku: index for index, sku in enumerate(self.skus)}
        self.word_vectorizer = joblib.load(self.artifact_dir / "word_tfidf.joblib")
        self.char_vectorizer = joblib.load(self.artifact_dir / "char_tfidf.joblib")
        self.word_matrix = joblib.load(self.artifact_dir / "word_product_matrix.joblib")
        self.char_matrix = joblib.load(self.artifact_dir / "char_product_matrix.joblib")

        history_payload = json.loads(
            (self.artifact_dir / "click_history.json").read_text(encoding="utf-8")
        )
        self.click_history = history_payload["click_history"]
        self.popularity = json.loads(
            (self.artifact_dir / "popularity.json").read_text(encoding="utf-8")
        )
        hybrid_config = json.loads(
            (self.artifact_dir / "hybrid_config.json").read_text(encoding="utf-8")
        )
        self.weights = hybrid_config["weights"]
        self.model_name = hybrid_config["model_name"]

        self.semantic_index = faiss.read_index(str(self.artifact_dir / "semantic.index"))
        self.semantic_embeddings = self.semantic_index.reconstruct_n(
            0, self.semantic_index.ntotal
        )
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self._semantic_model: SentenceTransformer | None = None

    @property
    def semantic_model(self) -> SentenceTransformer:
        if self._semantic_model is None:
            self._semantic_model = SentenceTransformer(self.model_name, device=self.device)
        return self._semantic_model

    def score(self, query: str) -> pd.DataFrame:
        query_text = normalize_text(query)
        query_key = normalize_query(query)
        if not query_text:
            query_text = "xbox game"

        word = (self.word_vectorizer.transform([query_text]) @ self.word_matrix.T).toarray()[0]
        char = (self.char_vectorizer.transform([query_text]) @ self.char_matrix.T).toarray()[0]
        query_embedding = self.semantic_model.encode(
            [query_text], normalize_embeddings=True, convert_to_numpy=True, show_progress_bar=False
        ).astype("float32")
        semantic = (query_embedding @ self.semantic_embeddings.T)[0]

        exact = np.zeros(len(self.products), dtype="float32")
        click_counts = self.click_history.get(query_key, {})
        maximum = max(click_counts.values(), default=1)
        for sku, count in click_counts.items():
            if str(sku) in self.sku_to_position:
                exact[self.sku_to_position[str(sku)]] = count / maximum

        popularity = np.array(
            [float(self.popularity.get(sku, 0.0)) for sku in self.skus], dtype="float32"
        )
        final = (
            self.weights["exact"] * exact
            + self.weights["word"] * word
            + self.weights["char"] * char
            + self.weights["semantic"] * semantic
            + self.weights["popularity"] * popularity
        )

        result = self.products[["sku", "title", "category"]].copy()
        result["score"] = final
        result["exact"] = exact
        result["lexical"] = 0.5 * word + 0.5 * char
        result["semantic"] = semantic
        result["popularity"] = popularity
        return result

    def recommend(self, query: str, k: int = 5) -> list[dict[str, Any]]:
        scored = self.score(query)
        positions = top_unique_indices(scored["score"].to_numpy(), self.skus, k)
        records = scored.iloc[positions].copy()
        numeric_columns = ["score", "exact", "lexical", "semantic", "popularity"]
        records[numeric_columns] = records[numeric_columns].round(6)
        return records.to_dict(orient="records")

