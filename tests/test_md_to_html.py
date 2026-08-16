from pathlib import Path

from src.md_to_html import markdown_to_html


def test_renders_markdown_with_escaped_title(tmp_path: Path) -> None:
    template = tmp_path / "report.html"
    template.write_text("<title>$title</title><main>$content</main>", encoding="utf-8")

    result = markdown_to_html("# 结果\n\n| A | B |\n|---|---|\n| 1 | 2 |", "A < B", template)

    assert "<title>A &lt; B</title>" in result
    assert "<h1>结果</h1>" in result
    assert "<table>" in result


def test_raw_html_from_model_is_not_executable(tmp_path: Path) -> None:
    template = tmp_path / "report.html"
    template.write_text("<main>$content</main>", encoding="utf-8")

    result = markdown_to_html("# 结果\n\n<script>alert('x')</script>", "报告", template)

    assert "<script>" not in result
    assert "&lt;script&gt;" in result


def test_markdown_attributes_and_unsafe_urls_are_removed(tmp_path: Path) -> None:
    template = tmp_path / "report.html"
    template.write_text("<main>$content</main>", encoding="utf-8")

    result = markdown_to_html(
        "[危险链接](javascript:alert(1)){onclick=alert(2)}\n\n"
        "![远程图片](https://tracker.example/pixel){onerror=alert(3)}",
        "报告",
        template,
    )

    assert "javascript:" not in result
    assert "onclick" not in result
    assert "onerror" not in result
    assert "<img" not in result
