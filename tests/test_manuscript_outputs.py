from pathlib import Path

from PIL import Image

from scripts.manuscript.build_manuscript_assets import build_figures


EXPECTED_FIGURES = [
    "figure_1_pipeline.png",
    "figure_2_corpus_collaboration.png",
    "figure_3_mixed_leadership.png",
    "figure_4_regional_hindex.png",
    "figure_5_country_hindex.png",
]


def test_manuscript_figures_exist_and_are_readable(tmp_path: Path):
    build_figures(tmp_path)

    for filename in EXPECTED_FIGURES:
        path = tmp_path / filename
        assert path.exists()
        with Image.open(path) as image:
            assert image.width >= 1600
            assert image.height >= 900


def test_pipeline_svg_is_deterministic_and_has_no_timestamp(tmp_path: Path):
    build_figures(tmp_path)

    svg = (tmp_path / "figure_1_pipeline.svg").read_text(encoding="utf-8")
    assert "<svg" in svg
    assert "<dc:date>" not in svg
    assert "2026-" not in svg
