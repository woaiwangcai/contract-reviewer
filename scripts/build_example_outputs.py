from __future__ import annotations

from pathlib import Path

from src.docx_to_md import docx_to_markdown
from src.md_to_html import markdown_to_html


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    examples = ROOT / "examples"
    contract_markdown = docx_to_markdown(examples / "sample_contract.docx")
    (examples / "sample_contract.md").write_text(contract_markdown, encoding="utf-8")

    review_markdown = (examples / "sample_review.md").read_text(encoding="utf-8")
    review_html = markdown_to_html(
        review_markdown,
        "虚构示例合同 - 合同审查报告",
        ROOT / "templates" / "report.html",
    )
    (examples / "sample_review.html").write_text(review_html, encoding="utf-8")


if __name__ == "__main__":
    main()
