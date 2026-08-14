import json
from pathlib import Path

from src.artifact_loader import build_manifest, validate_manifest


def test_manifest_detects_modified_artifact(tmp_path: Path) -> None:
    artifact = tmp_path / "model.bin"
    artifact.write_bytes(b"model-v1")
    manifest = build_manifest(tmp_path, [artifact.name], {"source": "test"})
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    assert validate_manifest(tmp_path) == []

    artifact.write_bytes(b"model-v2")
    assert validate_manifest(tmp_path) == ["sha256:model.bin"]

