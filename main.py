from __future__ import annotations

import argparse
import sys
from pathlib import Path

from dotenv import load_dotenv

from src.model_client import ModelConfigurationError
from src.version import VERSION
from src.workflow import ReviewWorkflowError, run_review


PROJECT_ROOT = Path(__file__).resolve().parent


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="将 DOCX 合同转换为 Markdown，调用模型审查，并生成 Markdown/HTML 报告。"
    )
    parser.add_argument("--input", required=True, type=Path, help="待审查的 .docx 文件")
    parser.add_argument(
        "--skill",
        type=Path,
        default=PROJECT_ROOT / "skills" / "contract_review.md",
        help="审查 Skill 文件",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=PROJECT_ROOT / "output",
        help="报告输出目录",
    )
    parser.add_argument(
        "--env-file",
        type=Path,
        default=PROJECT_ROOT / ".env",
        help="模型配置文件",
    )
    parser.add_argument("--version", action="version", version=f"contract-reviewer {VERSION}")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    load_dotenv(args.env_file)

    try:
        artifacts = run_review(
            input_path=args.input,
            skill_path=args.skill,
            output_dir=args.output,
            template_path=PROJECT_ROOT / "templates" / "report.html",
        )
    except (ModelConfigurationError, ReviewWorkflowError) as exc:
        print(f"错误：{exc}", file=sys.stderr)
        return 1

    print("审查完成")
    print(f"Markdown：{artifacts.markdown_path.resolve()}")
    print(f"HTML：{artifacts.html_path.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
