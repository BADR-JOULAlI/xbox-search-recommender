"""Explicit, private-by-default publication of approved model artifacts."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

APPROVED_FILENAMES = {
    "manifest.json",
    "hybrid_config.json",
    "word_tfidf.joblib",
    "char_tfidf.joblib",
    "word_product_matrix.joblib",
    "char_product_matrix.joblib",
    "semantic.index",
    "semantic_skus.json",
    "click_history.json",
    "popularity.json",
    "products.csv",
}


def collect_publishable_files(artifact_dir: Path) -> list[Path]:
    """Return only explicitly allow-listed artifact files."""
    artifact_dir = Path(artifact_dir)
    return sorted(
        path
        for path in artifact_dir.iterdir()
        if path.is_file() and path.name in APPROVED_FILENAMES
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-id", required=True)
    parser.add_argument("--artifact-dir", type=Path, default=Path("artifacts"))
    parser.add_argument("--private", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--confirm-license", action="store_true")
    parser.add_argument("--push", action="store_true")
    args = parser.parse_args()

    files = collect_publishable_files(args.artifact_dir)
    total_bytes = sum(path.stat().st_size for path in files)
    print(f"{len(files)} fichiers autorisés, {total_bytes / 1024**2:.2f} MiB")
    for path in files:
        print(f"- {path.name}: {path.stat().st_size} octets")

    if not args.push:
        print("Dry-run uniquement. Ajoutez --push après validation explicite.")
        return
    if not args.confirm_license:
        raise SystemExit(
            "Publication refusée : ajoutez --confirm-license après vérification juridique."
        )
    token = os.getenv("HF_TOKEN")
    if not token:
        raise SystemExit("HF_TOKEN absent de l'environnement.")

    from huggingface_hub import HfApi

    api = HfApi(token=token)
    api.create_repo(repo_id=args.repo_id, repo_type="model", private=args.private, exist_ok=True)
    for path in files:
        api.upload_file(
            path_or_fileobj=path,
            path_in_repo=path.name,
            repo_id=args.repo_id,
            repo_type="model",
        )
    model_card = Path("MODEL_CARD.md")
    if model_card.exists():
        api.upload_file(
            path_or_fileobj=model_card,
            path_in_repo="README.md",
            repo_id=args.repo_id,
            repo_type="model",
        )
    print(f"Publication terminée : https://huggingface.co/{args.repo_id}")


if __name__ == "__main__":
    main()
