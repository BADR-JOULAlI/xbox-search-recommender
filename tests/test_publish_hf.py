from pathlib import Path

from src.publish_hf import collect_publishable_files


def test_publish_allowlist_excludes_raw_data(tmp_path: Path) -> None:
    (tmp_path / "manifest.json").write_text("{}", encoding="utf-8")
    (tmp_path / "train.csv").write_text("private", encoding="utf-8")
    selected = collect_publishable_files(tmp_path)
    assert [path.name for path in selected] == ["manifest.json"]

