"""Dataset discovery and robust readers for the Kaggle competition files."""

from __future__ import annotations

import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from src.preprocessing import coerce_sku


@dataclass(frozen=True)
class CompetitionFiles:
    train: Path
    test: Path
    products: Path
    popular_skus: Path | None = None


def discover_competition_files(raw_dir: Path) -> CompetitionFiles | None:
    """Find the required files recursively, or return None when data is absent."""
    raw_dir = Path(raw_dir)

    def first(name: str) -> Path | None:
        return next(iter(raw_dir.rglob(name)), None)

    train = first("train.csv")
    test = first("test.csv")
    products = first("small_product_data.xml")
    if not all((train, test, products)):
        return None
    return CompetitionFiles(
        train=train,
        test=test,
        products=products,
        popular_skus=first("popular_skus.csv"),
    )


def read_csv_as_strings(path: Path) -> pd.DataFrame:
    """Read a competition CSV without losing identifiers or empty strings."""
    frame = pd.read_csv(path, dtype=str, keep_default_na=False, encoding_errors="replace")
    frame.columns = [str(column).strip().lower() for column in frame.columns]
    if "sku" in frame.columns:
        frame["sku"] = frame["sku"].map(coerce_sku)
    return frame


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1].lower()


def parse_products_xml(path: Path) -> pd.DataFrame:
    """Parse product records without assuming a namespace or strict XML shape."""
    aliases = {
        "sku": ("sku",),
        "title": ("name", "title"),
        "description": ("description", "shortdescription", "longdescription"),
        "category": ("category", "class", "department"),
        "price": ("price", "saleprice", "regularprice"),
        "release_date": ("releasedate", "release_date"),
    }
    records: list[dict[str, str]] = []
    for _, element in ET.iterparse(path, events=("end",)):
        children = list(element)
        child_map: dict[str, str] = {}
        for child in children:
            name = _local_name(child.tag)
            text = " ".join("".join(child.itertext()).split())
            if text and name not in child_map:
                child_map[name] = text
        sku = next((child_map.get(name, "") for name in aliases["sku"] if child_map.get(name)), "")
        if sku:
            record = {"sku": coerce_sku(sku)}
            for target, names in aliases.items():
                if target == "sku":
                    continue
                record[target] = next(
                    (child_map.get(name, "") for name in names if child_map.get(name)),
                    "",
                )
            records.append(record)
            element.clear()
    if not records:
        raise ValueError(f"Aucun produit avec SKU trouvé dans {path}")
    return pd.DataFrame.from_records(records).drop_duplicates(subset="sku", keep="first")

