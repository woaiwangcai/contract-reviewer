from __future__ import annotations

from html import escape
from pathlib import Path
from string import Template

import markdown
import nh3


class HtmlRenderError(RuntimeError):
    """Raised when the HTML report template cannot be rendered."""


ALLOWED_TAGS = {
    "a",
    "blockquote",
    "br",
    "code",
    "em",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "hr",
    "li",
    "ol",
    "p",
    "pre",
    "strong",
    "table",
    "tbody",
    "td",
    "th",
    "thead",
    "tr",
    "ul",
}


def markdown_to_html(markdown_text: str, title: str, template_path: Path) -> str:
    template_path = Path(template_path)
    if not template_path.is_file():
        raise HtmlRenderError(f"找不到 HTML 模板：{template_path}")

    try:
        template = Template(template_path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise HtmlRenderError(f"无法读取 HTML 模板：{exc}") from exc

    safe_markdown = escape(markdown_text, quote=False)
    rendered = markdown.markdown(
        safe_markdown,
        extensions=["extra", "sane_lists"],
        output_format="html5",
    )
    body = nh3.clean(
        rendered,
        tags=ALLOWED_TAGS,
        attributes={"a": {"href", "title"}},
        url_schemes={"http", "https", "mailto"},
        strip_comments=True,
    )
    try:
        return template.substitute(title=escape(title), content=body)
    except (KeyError, ValueError) as exc:
        raise HtmlRenderError("HTML 模板包含无效占位符。") from exc
