from __future__ import annotations

import os
import re
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from src.docx_to_md import DocxConversionError, docx_to_markdown
from src.md_to_html import HtmlRenderError, markdown_to_html
from src.model_client import ModelCallError, review_contract


class ReviewWorkflowError(RuntimeError):
    """Raised when the review workflow cannot complete."""


@dataclass(frozen=True)
class ReviewArtifacts:
    markdown_path: Path
    html_path: Path


def _safe_stem(value: str) -> str:
    stem = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", value).strip(" .")
    return stem if any(character.isalnum() for character in stem) else "contract"


def _read_skill(path: Path) -> str:
    path = Path(path)
    if not path.is_file():
        raise ReviewWorkflowError(f"找不到审查 Skill：{path}")
    try:
        content = path.read_text(encoding="utf-8").strip()
    except (OSError, UnicodeError) as exc:
        raise ReviewWorkflowError(f"无法读取审查 Skill：{exc}") from exc
    if not content:
        raise ReviewWorkflowError("审查 Skill 不能为空。")
    return content


def _next_report_paths(output_dir: Path, stem: str) -> tuple[Path, Path]:
    sequence = 1
    while True:
        suffix = "" if sequence == 1 else f"-{sequence}"
        markdown_path = output_dir / f"{stem}-review{suffix}.md"
        html_path = output_dir / f"{stem}-review{suffix}.html"
        if not markdown_path.exists() and not html_path.exists():
            return markdown_path, html_path
        sequence += 1


def _write_report_pair(
    markdown_path: Path,
    html_path: Path,
    markdown_text: str,
    html_text: str,
) -> None:
    temporary_paths: list[Path] = []
    committed_paths: list[Path] = []
    try:
        for target, content in ((markdown_path, markdown_text), (html_path, html_text)):
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=target.parent,
                prefix=f".{target.name}.",
                suffix=".tmp",
                delete=False,
            ) as handle:
                handle.write(content)
                temporary_paths.append(Path(handle.name))

        for temporary, target in zip(
            temporary_paths,
            (markdown_path, html_path),
            strict=True,
        ):
            os.replace(temporary, target)
            committed_paths.append(target)
    except OSError:
        for path in committed_paths:
            path.unlink(missing_ok=True)
        raise
    finally:
        for path in temporary_paths:
            path.unlink(missing_ok=True)


def run_review(
    input_path: Path,
    skill_path: Path,
    output_dir: Path,
    template_path: Path,
    reviewer: Callable[[str, str], str] | None = None,
) -> ReviewArtifacts:
    try:
        contract_markdown = docx_to_markdown(Path(input_path))
        skill = _read_skill(Path(skill_path))
        review_markdown = (reviewer or review_contract)(skill, contract_markdown)
        if not review_markdown.strip():
            raise ReviewWorkflowError("模型返回了空审查结果。")

        title = f"{Path(input_path).stem} - 合同审查报告"
        html = markdown_to_html(review_markdown, title, Path(template_path))
    except (DocxConversionError, ModelCallError, HtmlRenderError) as exc:
        raise ReviewWorkflowError(str(exc)) from exc

    output_dir = Path(output_dir)
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        stem = _safe_stem(Path(input_path).stem)
        markdown_path, html_path = _next_report_paths(output_dir, stem)
        _write_report_pair(markdown_path, html_path, review_markdown, html)
    except OSError as exc:
        raise ReviewWorkflowError(f"无法写入报告：{exc}") from exc

    return ReviewArtifacts(markdown_path=markdown_path, html_path=html_path)
