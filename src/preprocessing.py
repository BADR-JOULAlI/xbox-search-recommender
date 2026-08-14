"""Small reusable preprocessing primitives shared by notebooks and the app."""

from __future__ import annotations

import math
import re
import unicodedata
from typing import Any

_NON_ALNUM = re.compile(r"[^a-z0-9]+")
_TRAILING_DECIMAL = re.compile(r"^([0-9]+)\.0+$")


def normalize_text(value: Any) -> str:
    """Normalize free text while retaining word boundaries."""
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return ""
    text = unicodedata.normalize("NFKD", str(value))
    text = text.encode("ascii", "ignore").decode("ascii").lower()
    return " ".join(_NON_ALNUM.sub(" ", text).split())


def normalize_query(value: Any) -> str:
    """Normalize a query for exact click-history matching."""
    return normalize_text(value).replace(" ", "")


def coerce_sku(value: Any) -> str:
    """Return a stable string SKU and undo accidental CSV float coercion."""
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return ""
    sku = str(value).strip()
    match = _TRAILING_DECIMAL.fullmatch(sku)
    return match.group(1) if match else sku

