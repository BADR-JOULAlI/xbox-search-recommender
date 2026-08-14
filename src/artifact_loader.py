"""Integrity helpers for local model artifacts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        while chunk := stream.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def build_manifest(artifact_dir: Path, filenames: list[str], metadata: dict[str, Any]) -> dict:
    artifact_dir = Path(artifact_dir)
    files: dict[str, dict[str, int | str]] = {}
    for filename in filenames:
        path = artifact_dir / filename
        if not path.is_file():
            raise FileNotFoundError(path)
        files[filename] = {"bytes": path.stat().st_size, "sha256": sha256_file(path)}
    return {"schema_version": 1, "metadata": metadata, "files": files}


def validate_manifest(artifact_dir: Path, manifest_path: Path | None = None) -> list[str]:
    artifact_dir = Path(artifact_dir)
    path = manifest_path or artifact_dir / "manifest.json"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    errors: list[str] = []
    for filename, expected in manifest["files"].items():
        artifact = artifact_dir / filename
        if not artifact.is_file():
            errors.append(f"missing:{filename}")
        elif artifact.stat().st_size != expected["bytes"]:
            errors.append(f"size:{filename}")
        elif sha256_file(artifact) != expected["sha256"]:
            errors.append(f"sha256:{filename}")
    return errors

