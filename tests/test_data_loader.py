from pathlib import Path

from src.data_loader import discover_competition_files, parse_products_xml


def test_discover_requires_all_core_files(tmp_path: Path) -> None:
    (tmp_path / "train.csv").write_text("sku,query\n1,halo\n", encoding="utf-8")
    assert discover_competition_files(tmp_path) is None

    (tmp_path / "test.csv").write_text("query\nhalo\n", encoding="utf-8")
    (tmp_path / "small_product_data.xml").write_text("<products />", encoding="utf-8")
    files = discover_competition_files(tmp_path)
    assert files is not None
    assert files.train.name == "train.csv"


def test_parse_products_xml_supports_namespaces(tmp_path: Path) -> None:
    xml = """<?xml version="1.0" encoding="utf-8"?>
    <catalog xmlns="urn:test">
      <product>
        <sku>123.0</sku>
        <name>Halo</name>
        <description>Science fiction shooter</description>
        <salePrice>19.99</salePrice>
      </product>
    </catalog>
    """
    path = tmp_path / "products.xml"
    path.write_text(xml, encoding="utf-8")

    products = parse_products_xml(path)
    assert products.loc[0, "sku"] == "123"
    assert products.loc[0, "title"] == "Halo"
    assert products.loc[0, "price"] == "19.99"

